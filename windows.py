import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AbsAppWindow(Gtk.Window):

    #TODO - set up params to take from main app, config,
    # related to widget scaling etc
    def __init__(self, next_att_timer_scale):

        if self.__class__.__name__ == 'AbsAppWindow':
            raise NotImplementedError('Abstract base class') 
    
        screen = self.get_screen()
        self.screen_width = screen.width
        self.screen_height = screen.height

        self.next_att_timer_label_size = int(self.screen_height * next_att_timer_scale) * 1000

        self.black_color = Gdk.Color(red=0, green=0, blue=0)
        self.bg_eventbox = Gtk.EventBox()
        self.add(bg_eventbox)
        
        Gtk.Window.__init__(self)

    def update_next_att_timer(self, timer_str):
        #TODO


class LiftTimerWindow(AbsAppWindow):

    def __init__(self, widget_scaling_dict):
    
        AbsAppWindow.__init__(self, widget_scaling_dict['next_att_timer_scale'])

        self.lift_timer_label_size = self.screen_height * widget_scaling_dict['lift_timer_scale']
        self.lift_timer_label = Gtk.Label()
        self.bg_eventbox.add(self.lift_timer_label)

    def update_lift_timer(self, timer_str):

        self.lift_timer_label.set_markup('<span size="{}" foreground="white">{}</span>'.format(self.lift_timer_label_size, timer_str)) 
        

class LightsWindow(AbsAppWindow):

    def __init__(self, widget_scaling_dict):
    
        AbsAppWindow.__init__(self, widget_scaling_dict['next_att_timer_scale'])

        #TODO - method(s) for showing lights, next att timer
