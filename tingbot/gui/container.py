import pygame
from ..input import HitArea
from ..graphics import _xy_subtract,_xy_add
from .widget import Widget
from .slider import Slider
from .util import clamp

class Container(Widget):
    """This is a base class for both Panels and ScrollAreas
    This implements container which can hold and keep track of other widgets and allows you
    to easily draw or hide all contained widgets and also manageds any incoming inputs"""
    def __init__(self,xy,size,align="center",parent=None,style=None):
        """Initialise this container. It creates it's own subsurface for drawing on
        xy, size and align specify the position of the widget
        style specifies any look and appearance needed
        if this widget will live in a sub-container, such as ScrollArea, specify this with parent
        otherwise it will be attached to the main screen
        xy is relative to the parent widget (or screen)
        """
        super(Container,self).__init__(xy,size,align,parent,style)
        self.children = []
        self.hit_areas = []
        self.active_hit_areas = []
               
    def add_child(self,widget):
        """Add a child widget to this container"""
        self.children.append(widget)
        offset = widget.surface.get_offset()
        rect = pygame.Rect(offset,widget.size)
        self.hit_areas.append(HitArea(rect,widget._touch))
        
    def remove_child(self,widget):
        """Remove a specified child from this widget"""
        self.hit_areas[:] = [x for x in self.hit_areas if x.callback.__self__ is not widget]
        self.active_hit_areas[:] = [x for x in self.active_hit_areas if x.callback.__self__ is not widget]
        self.children.remove(widget)
    
    def remove_all(self):
        """Remove all children from this widget"""
        self.children[:] = []
        self.hit_areas[:] = []    
        
    def on_touch(self,xy,action):
        """distribute touch events to relevant widgets, offset relative to each widget"""
        if action=='down':
            for hit_area in self.hit_areas:
                if hit_area.rect.collidepoint(xy):
                    self.active_hit_areas.append(hit_area)
                    pos = _xy_subtract(xy,hit_area.rect.topleft)
                    hit_area.callback(pos,'down')
        elif action in ('move','up'):
            for hit_area in self.active_hit_areas:
                pos = _xy_subtract(xy,hit_area.rect.topleft)
                hit_area.callback(pos, action)
        if action=='up':
            self.active_hit_areas[:] = []

    def update(self,upwards=True,downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """
        if self.visible:
            if downwards:
                for child in self.children:
                    child.update(upwards=False,downwards=True)
            self.draw()
        if upwards:
            if hasattr(self.parent,'update'):
                self.parent.update()
            

class Panel(Container):
    """Use this class to specify groups of widgets that can be turned on and off together
    
    Style Attributes:
        bg_color: background color"""
    def draw(self):
        """ no action needed on draw"""
        pass        
        
    def update(self,upwards=True,downwards=False):
        #clear contents before drawing
        if self.visible and downwards:
            self.fill(self.style.bg_color)
        super(Panel,self).update(upwards,downwards)
        
class VirtualPanel(Panel):
    """This class implements a virtual panel"""
    def __init__(self,size,parent):
        super(VirtualPanel,self).__init__((0,0),size,"topleft",parent)
        self.init_size = size
        
    def _create_surface(self):
        return pygame.Surface(self.init_size,0,self.parent.surface)
        
class ViewPort(Container):
    """the viewport is a container that only has one child, a VirtualPanel"""
    def __init__(self,xy,size,align="center",parent = None, canvas_size = None,vslider = None,hslider = None):
        super(ViewPort,self).__init__(xy,size,align,parent)
        self.panel = VirtualPanel(canvas_size,self)
        self.position = [0,0]
        self.max_position = [max(0,canvas_size[0]-size[0]),max(0,canvas_size[1]-size[1])]
        self.vslider = vslider
        self.hslider = hslider
        if self.vslider:
            self.vslider.max_val = self.max_position[1]
            self.vslider.value = self.max_position[0]
            self.vslider.change_callback = self.vslider_cb
        if self.hslider:
            self.hslider.max_val = self.max_position[0]
            self.hslider.change_callback = self.set_x

    def set_x(self,value):
        value = clamp(0,self.max_position[0],int(value))
        self.position[0] = value
        if self.hslider:
            self.hslider.value = value
        self.update()

    def set_y(self,value,inverted=False):
        value = clamp(0,self.max_position[1],int(value))
        self.position[1] = int(value)
        if self.vslider:
            self.vslider.value = self.max_position[1]-value
        self.update()

    def vslider_cb(self,value):
        value = self.max_position[1]-value
        self.set_y(value)    

    def on_touch(self,xy,action):
        #translate xy positions to account for panel position, and pass on to the panel for processing
        self.panel.on_touch(_xy_add(xy,self.position),action)
        
    def draw(self):           
        self.surface.blit(self.panel.surface,(0,0),pygame.Rect(self.position,self.size))
        

class ScrollArea(Container):
    """Use this class to specify a sub-window with (optional) scrollbars
    style: specify the style of your sliders
    canvas_size: specify the size of the underlying window

    Style Attributes:
        scrollbar_width: width of the scrollbars
        slider_line_color: color of the line
        slider_handle_color: color of the handle
    """    
    def __init__(self,xy,size,align="center",parent=None,style = None,canvas_size=None):
        if canvas_size == None:
            raise ValueError("canvas_size must be specified")
        super(ScrollArea,self).__init__(xy,size,align,parent,style)
        rect = pygame.Rect((0,0),size)
        self.top_surface = self.surface
        self.vslider = None
        self.hslider = None
        if canvas_size[0]>rect.right:
            rect.height -= self.style.scrollbar_width
            hscrollbar = True
        if canvas_size[1]>rect.bottom:
            rect.width -= self.style.scrollbar_width
            vscrollbar = True
        if canvas_size[0]>rect.right and not hscrollbar:
            rect.height -= self.style.scrollbar_width
            hscrollbar = True
        if vscrollbar:
            self.vslider = Slider(xy = rect.topright, size = (self.style.scrollbar_width,rect.bottom), align = 'topleft',parent=self,style=style)
        if hscrollbar:
            self.hslider = Slider(xy = rect.bottomleft, size = (rect.right,self.style.scrollbar_width), align = 'topleft',parent=self,style=style)
        self.viewport = ViewPort((0,0),rect.bottomright,
                                 align=align,
                                 parent=self,
                                 canvas_size=canvas_size,
                                 vslider = self.vslider,
                                 hslider = self.hslider)
        
    def update(self,upwards=True,downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """
        super(ScrollArea,self).update(upwards,downwards)
        if self.visible:
            if self.vslider:
                self.vslider.update(upwards=False)
            if self.hslider:
                self.hslider.update(upwards=False)

    def draw(self):
        #all drawing functions are provided by this classes children
        pass
            
    @property
    def scrolled_area(self):
        return self.viewport.panel



