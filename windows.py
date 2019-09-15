import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class AbsAppWindow(Gtk.Window):

    def __init__(self, next_att_timer_scale, ui_handler):

        if self.__class__.__name__ == 'AbsAppWindow':
            raise NotImplementedError('Abstract base class') 
        
        Gtk.Window.__init__(self)
    
        # disable mouse movement and clicks in case we use them as controllers
        self.connect('button-press-event', ui_handler.null_handler)
        self.connect('motion-notify-event', ui_handler.null_handler)

        screen = self.get_screen()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        self.next_att_timer_label_size = self.scale(self.screen_height, next_att_timer_scale) * 1000

        self.black_color = Gdk.Color(red=0, green=0, blue=0)
        self.bg_eventbox = Gtk.EventBox()
        self.bg_eventbox.modify_bg(Gtk.StateType.NORMAL, self.black_color)
        self.add(self.bg_eventbox)
        self.vbox = Gtk.VBox(False, 4)
        self.bg_eventbox.add(self.vbox)
        self.bg_eventbox.show()
        self.vbox.show()
 
        self.fullscreen()

    def scale(self, dimension, factor):

        scaled_dimension = int(int(dimension) * float(factor))
        
        return scaled_dimension

    def add_next_att_timer(self):

        # can't just add this stuff in the constructor cause different stuff goes in first, in different windows
        self.next_att_timer_label = Gtk.Label()
        self.next_att_timer_box = Gtk.Box()
        self.next_att_timer_box.pack_end(self.next_att_timer_label, False, False, 0)
        self.vbox.pack_start(self.next_att_timer_box, False, False, 0)

    def update_next_att_timer(self, timer_str):

        #DEBUG
        print('about to update next attempt timer with string {} at size {}'.format(timer_str, self.next_att_timer_label_size))
        print('next attempt timer label is visible: {}'.format(self.next_att_timer_label.props.visible))
    
        self.next_att_timer_label.set_markup('<span size="{}" foreground="white">Next attempt submission: {}</span>'.format(self.next_att_timer_label_size, timer_str))   

    def show_next_att_timer(self):
        self.next_att_timer_box.show()
        self.next_att_timer_label.show()

        #DEBUG
        print('called show_next_att_timer(), next attempt timer is now visible: {}'.format(self.next_att_timer_label.props.visible))

    def hide_next_att_timer(self):
        self.next_att_timer_box.hide()
        self.next_att_timer_label.hide()


class LiftTimerWindow(AbsAppWindow):

    def __init__(self, widget_scaling_dict):
    
        AbsAppWindow.__init__(self, widget_scaling_dict['next_att_timer_scale'])

        self.lift_timer_label_size = self.scale(self.screen_height, widget_scaling_dict['lift_timer_scale']) * 1000
        self.lift_timer_label = Gtk.Label()
        self.vbox.pack_start(self.lift_timer_label, True, False, 0)

        self.add_next_att_timer()

    def show_lift_timer(self):

        #DEBUG
        print('about to show lift timer label')

        self.lift_timer_label.show()
        self.next_att_timer_box.show()
        self.show()

    def update_lift_timer(self, timer_str):

        #DEBUG
        print('about to update lift timer label with {} at size {}'.format(timer_str, self.lift_timer_label_size))

        self.lift_timer_label.set_markup('<span size="{}" foreground="white">{}</span>'.format(self.lift_timer_label_size, timer_str)) 
        

class LightsWindow(AbsAppWindow):

    def __init__(self, widget_scaling_dict, light_image_dict):
    
        AbsAppWindow.__init__(self, widget_scaling_dict['next_att_timer_scale'])

        light_width = self.scale(self.screen_width, widget_scaling_dict['light_scale'])
        light_height = light_width
       
        self.red_light_pixbuf = GdkPixbuf.Pixbuf.new_from_file(light_image_dict['red']).scale_simple(light_width, light_height, GdkPixbuf.InterpType.BILINEAR)
        self.white_light_pixbuf = GdkPixbuf.Pixbuf.new_from_file(light_image_dict['white']).scale_simple(light_width, light_height, GdkPixbuf.InterpType.BILINEAR)  

        self.light_box = Gtk.Box(spacing=self.scale(self.screen_width, widget_scaling_dict['light_spacing_scale']))

        self.light_dict = {}
        for k in ['left', 'head', 'right']:
            self.light_dict[k] = Gtk.Image()
            self.light_box.pack_start(self.light_dict[k], True, False, 0)
        
        self.vbox.pack_start(self.light_box, True, False, 0)

        self.add_next_att_timer()

    def show_lights(self, light_state_obj):

        #DEBUG
        print('about to show lights')

        if light_state_obj.is_complete():
            state_dict = light_state_obj.get_state()
            
            for position in ['left', 'head', 'right']:
                if state_dict[position] == True:

                    #DEBUG
                    print('setting white light for position {}'.format(position))

                    self.light_dict[position].set_from_pixbuf(self.white_light_pixbuf)
                elif state_dict[position] == False:

                    #DEBUG
                    print('setting red light for position {}'.format(position))

                    self.light_dict[position].set_from_pixbuf(self.red_light_pixbuf)

                self.light_dict[position].show()
 
            self.light_box.show()
            self.vbox.show()
            self.show()

    def hide_lights(self):
        
        for position in ['left', 'head', 'right']:
            self.light_dict[position].hide()


class MapControllersWindow(AbsAppWindow):

    def __init__(self, widget_scaling_dict):

        AbsAppWindow.__init__(self, widget_scaling_dict['next_att_timer_scale'])

        self.prompt_label = Gtk.Label()
        self.prompt_label_size = self.scale(self.screen_height, widget_scaling_dict['controller_prompt_scale']) * 1000
        self.vbox.pack_start(self.prompt_label, True, False, 0)

    def show_controller_prompt(self, position):

        #DEBUG
        #print('About to set controller prompt for position {} at size {}'.format(position, self.prompt_label_size))

        self.prompt_label.set_markup('<span size="{}" foreground="white">Press any button on the {} controller</span>'.format(self.prompt_label_size, position))
        self.prompt_label.show()
        self.vbox.show()
        self.show()

        #DEBUG
        #print('label visibility: {}, vbox visibility: {}, window visibility: {}'.format(self.prompt_label.props.visible, self.vbox.props.visible, self.props.visible))
