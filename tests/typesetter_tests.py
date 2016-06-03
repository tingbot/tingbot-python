# coding: utf8
import unittest, sys
from tingbot.typesetter import Typesetter

character_metrics = (0, 1, 0, 1, 1)
def metrics_for_string(string):
    ''' All characters are 1x1 for easy testability '''
    return (character_metrics, ) * len(string)

class TypesetterTestCase(unittest.TestCase):
    def assertRenders(self, input, expected_output, max_lines=sys.maxsize, max_width=sys.maxsize,
                      ellipsis='...', ellipsis_metrics=metrics_for_string('...')):
        t = Typesetter(input, metrics_for_string(input))

        lines = t.lines(
            max_lines=max_lines,
            max_width=max_width,
            ellipsis=ellipsis,
            ellipsis_metrics=ellipsis_metrics)

        self.assertEqual(expected_output, [l.string for l in lines])

    def test_trucate(self):
        self.assertRenders('12345678901234567890', ['1234567...', ], max_lines=1, max_width=10)

    def test_no_trucate(self):
        self.assertRenders('1234567890', ['1234567890', ], max_width=10)

    def test_midword_break(self):
        self.assertRenders('123456789012345', ['1234567890', '12345'], max_width=10)

    def test_word_break(self):
        self.assertRenders('asd asd asd asd', ['asd asd', 'asd asd'], max_width=10)

    def test_multiple_word_breaks(self):
        self.assertRenders('asd asd asd asd asd', ['asd asd', 'asd asd', 'asd'], max_width=10)

    def test_newline_break(self):
        self.assertRenders('asd asd\nasd asd', ['asd asd', 'asd asd'])

    def test_break_and_truncate(self):
        self.assertRenders('asd asd asd asd asd', ['asd asd', 'asd asd...'], max_lines=2, max_width=10)

    def test_zero_width(self):
        self.assertRenders('1234', ['1', '2', '3', '4'], max_width=0)

    def test_zero_width_and_truncate(self):
        self.assertRenders('1234', ['1', '2', '...'], max_width=0, max_lines=3)

    def test_single_line_zero_width_and_truncate(self):
        self.assertRenders('1234', ['...'], max_width=0, max_lines=1)

    def test_whitespace_after_newline(self):
        self.assertRenders('abc\n  def', ['abc', '  def'])

    def test_truncate_whitespace_single_line(self):
        self.assertRenders('abc       ', ['abc  ...'], max_width=8, max_lines=1)
