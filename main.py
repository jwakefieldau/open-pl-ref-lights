import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from configparser import ConfigParser

from windows import LiftTimerWindow, LightsWindow, MapControllersWindow
from event_handlers import TimerHandler, PollAndAct
from state import TimerState, LightsState, ControllersState
from controllers import button_maps

config_path = './config.cfg'

if __name__ == '__main__':

    config = ConfigParser()
    config.read_file(open(config_path))

    lift_timer_window = LiftTimerWindow(config['widget_scaling'])
    lights_window = LightsWindow(config['widget_scaling'], config['light_images'])
    map_controllers_window = MapControllersWindow(config['widget_scaling'])

    next_att_timer_state = TimerState()
    lift_timer_state = TimerState()

    light_state = LightsState()

    controllers_state = ControllersState()

    #TODO - change this when controller mapping is done
    poll_act_obj = PollAndAct(config['controllers'], button_maps, next_att_timer_state, lift_timer_state, light_state, lift_timer_window, lights_window)

    # is this fine enough resolution?
    GObject.timeout_add(100, poll_act_obj.poll)

    timer_handler = TimerHandler(lift_timer_window, lights_window, next_att_timer_state, lift_timer_state)
    GObject.timeout_add(1000, timer_handler.handle_tick)

    #show lift timer initially
    #TODO - show controller_map_window initially
    lift_timer_window.show()


    Gtk.main()

