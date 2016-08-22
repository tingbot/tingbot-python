#!/usr/bin/env python

from docopt import docopt
import os, textwrap, shutil, filecmp, subprocess, sys, logging
import paramiko
from .appdirs import AppDirs


class SSHSession(object):
    def __init__(self, hostname):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(SSHSession.IgnoreHostKeyPolicy())
        key_path = os.path.join(os.path.dirname(__file__), 'tingbot.key')
        self.client.connect(hostname, username='pi', key_filename=key_path)

    def exec_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)

        output = stdout.read()
        error_output = stderr.read()
        code = stdout.channel.recv_exit_status()

        if code != 0:
            raise SSHSession.RemoteCommandError(command, code, output, error_output)

    def put_dir(self, source, target):
        sftp = self.client.open_sftp()

        try:
            sftp.mkdir(target, 0755)

            for filename in os.listdir(source):
                local_path = os.path.join(source, filename)
                remote_path = '%s/%s' % (target, filename)

                if os.path.islink(local_path):
                    link_destination = os.readlink(local_path)
                    sftp.symlink(remote_path, link_destination)

                elif os.path.isfile(local_path):
                    sftp.put(local_path, remote_path)

                elif os.path.isdir(local_path):
                    self.put_dir(local_path, remote_path)
        finally:
            sftp.close()

    def close(self):
        self.client.close()

    class IgnoreHostKeyPolicy(object):
        def missing_host_key(self, client, hostname, key):
            return

    class RemoteCommandError(Exception):
        def __init__(self, command, code, output, error_output):
            self.command = command
            self.code = code
            self.output = output
            self.error_output = error_output
            message = 'Remote command %s failed with code %i. \n%s\n%s' % (
                command, code, output, error_output)
            super(SSHSession.RemoteCommandError, self).__init__(message)


def _app_exec_info(app_path, python_exe='python'):
    """ Returns a pair ([args], working_directory) """

    app_path = os.path.abspath(app_path)

    if os.path.isfile(app_path):
        return ([app_path], os.path.dirname(app_path))

    if os.path.isdir(app_path):
        main_file = os.path.join(app_path, 'main')
        if os.path.isfile(main_file):
            return ([main_file], app_path)

        main_py_file = os.path.join(app_path, 'main.py')
        if os.path.isfile(main_py_file):
            return ([python_exe, main_py_file], app_path)

    return (None, None)

def _exec(args, env):
    if sys.platform != 'win32':
        os.execvpe(args[0], args, env)
    else:
        # 'exec' on Windows doesn't have the same semantics - on Windows the calling process
        # returns as if it had exited. Here we simulate *nix 'exec' behaviour.

        # Ignore CTRL-C events as they're handled by the subprocess
        import signal
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        process = subprocess.Popen(args, env=env)
        process.wait()
        sys.exit(process.returncode)

def _run(app_path, extra_env=None):
    python_exe = build(app_path)

    args, working_directory = _app_exec_info(app_path, python_exe=python_exe)

    if args is None:
        raise ValueError('Tingbot app not found at %s' % app_path)

    env = os.environ.copy()

    if extra_env:
        env.update(extra_env)

    os.chdir(working_directory)
    _exec(args, env)

def simulate(app_path):
    _run(app_path)


def run(app_path, hostname):
    print 'tbtool: Connecting to Pi...'

    session = SSHSession(hostname)

    try:
        app_name = os.path.basename(app_path)

        app_install_location = '/tmp/tide/%s' % app_name
        app_install_folder = os.path.dirname(app_install_location)

        print 'tbtool: Setting up Pi...'
        session.exec_command('mkdir -p "%s"' % app_install_folder)

        print 'tbtool: Copying app to %s...' % app_install_location
        session.exec_command('sudo rm -rf "%s"' % app_install_location)
        session.put_dir(app_path, app_install_location)

        print 'tbtool: Starting app...'
        session.exec_command('tbopen "%s"' % app_install_location)
    finally:
        session.close()

def build(app_path):
    '''
    Installs the dependencies in requirements.txt into a virtualenv in the app directory
    Returns the path to the python executable that should be used to run the app.
    '''
    import virtualenv
    wheelhouse = os.path.join(AppDirs('Tingbot', 'Tingbot').user_cache_dir, 'Wheelhouse')

    if not os.path.exists(wheelhouse):
        os.makedirs(wheelhouse)

    requirements_txt_path = os.path.join(app_path, 'requirements.txt')
    venv_path = os.path.join(app_path, 'venv')
    _, venv_lib_dir, _, venv_bin_dir = virtualenv.path_locations(venv_path)
    venv_python_path = os.path.join(venv_bin_dir, 'python')
    venv_previous_requirements_path = os.path.join(venv_path, 'requirements.txt')

    if not os.path.isfile(requirements_txt_path):
        # delete the venv if it's there and use the system python
        clean(app_path)
        return 'python'

    # check that there's a virtualenv there and that it's got a working
    # version of python
    try:
        subprocess.check_call([
            venv_python_path,
            '-c', 'import sys; sys.exit(0)'
        ])
    except (OSError, subprocess.CalledProcessError):
        # we've got to build the virtualenv
        clean(app_path)
        print 'tbtool: Creating virtualenv...'
        virtualenv.create_environment(venv_path, site_packages=True,)

        # ignore the virtualenv when the app is tracked with git
        gitignore_path = os.path.join(venv_path, '.gitignore')
        with open(gitignore_path, 'w') as f:
            f.write(textwrap.dedent('''
                # Generated by tbtool.

                # Don't commit virtualenvs to git, because they contain platform-specific
                # code and don't relocate well.

                # '*' matches everything in this folder

                *
                '''))

    # if PYTHONPATH is defined (this is how Tide bundles packages on Mac and Linux),
    # the packages there have precidence over the packages in this virtualenv. That
    # prevents the user upgrading anything that's bundled, so we'll add the virtualenv's
    # packages in front of the existing PYTHONPATH.
    if 'PYTHONPATH' in os.environ:
        venv_site_packages = os.path.join(venv_lib_dir, 'site-packages')
        os.environ['PYTHONPATH'] = venv_site_packages + ':' + os.environ['PYTHONPATH']

    requirements_unchanged_since_last_run = (
        os.path.isfile(venv_previous_requirements_path)
        and filecmp.cmp(requirements_txt_path, venv_previous_requirements_path)
    )

    if not requirements_unchanged_since_last_run:
        print 'tbtool: Installing dependencies into virtualenv...'
        venv_pip_path = os.path.join(venv_bin_dir, 'pip')

        env = os.environ.copy()
        env['PIP_FIND_LINKS'] = 'file://%s' % wheelhouse
        env['PIP_WHEEL_DIR'] = wheelhouse

        subprocess.check_call([
                venv_python_path,
                '-m', 'pip',
                'install', '-r', requirements_txt_path,
            ],
            env=env
        )

        # copy requirements into the venv so we don't need to run pip every run
        shutil.copyfile(requirements_txt_path, venv_previous_requirements_path)

    return venv_python_path


def clean(app_path):
    venv_path = os.path.join(app_path, 'venv')
    shutil.rmtree(venv_path, ignore_errors=True)


def install(app_path, hostname):
    session = SSHSession(hostname)

    try:
        app_name = os.path.basename(app_path)

        app_install_location = '/apps/%s' % app_name

        print 'tbtool: Copying app to %s...' % app_install_location
        session.exec_command('sudo rm -rf "%s"' % app_install_location)
        session.put_dir(app_path, app_install_location)

        print 'tbtool: Preparing app...'
        session.exec_command('tbtool build "%s"' % app_install_location)

        print 'tbtool: Restarting springboard...'
        session.exec_command('tbopen /apps/home')

        print 'tbtool: App installed.'
    finally:
        session.close()


def tingbot_run(app_path):
    _run(app_path, extra_env={'TB_RUN_ON_LCD': '1'})


def main():
    args = docopt(textwrap.dedent('''
        Usage: 
          tbtool [-v] simulate <app>
          tbtool [-v] run <app> <hostname>
          tbtool [-v] install <app> <hostname>
          tbtool [-v] build <app>
          tbtool [-v] clean <app>
          tbtool [-v] tingbot_run <app>
          tbtool -h|--help

        Options:
          -v, --verbose             Output more information when errors occur

        Commands:
          simulate <app>            Runs the app in the simulator
          run <app> <hostname>      Runs the app on the Tingbot specified by hostname
          install <app> <hostname>  Installs the app on the Tingbot specified by
                                    hostname
          build <app>               If the app contains a requirements.txt file, creates
                                    a virtualenv with those packages installed. Not
                                    usually required to be called directly, building is
                                    automatic when using 'simulate', 'run' and 'install'.
          clean <app>               Removes temporary files in the app
          tingbot_run <app>         Used by tbprocessd to run Tingbot apps on the
                                    Tingbot itself. Users should probably use `tbopen'
                                    instead.
        '''))

    if args['--verbose']:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.CRITICAL+1)

    try:
        if not os.path.exists(args['<app>']):
            raise Exception("%s: no such file or directory" % args['<app>'])

        app_path = os.path.abspath(args['<app>'])

        if args['simulate']:
            simulate(app_path)

        elif args['run']:
            run(app_path, args['<hostname>'])

        elif args['install']:
            install(app_path, args['<hostname>'])

        elif args['build']:
            build(app_path)

        elif args['clean']:
            clean(app_path)

        elif args['tingbot_run']:
            tingbot_run(app_path)

    except Exception as e:
        for arg in e.args:
            if isinstance(arg, int) and arg == e.args[0]:
                sys.stderr.write('tbtool: %s error %i\n' % (e.__class__.__name__, arg))
            else:
                for line in str(arg).splitlines():
                    sys.stderr.write('tbtool: %s\n' % line)
        if args['--verbose']:
            import traceback
            traceback.print_exc(file=sys.stderr)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
