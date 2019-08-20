import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from configparser import ConfigParser

from windows import LiftTimerWindow, LightsWindow
from event_handlers import TimerHandler, PollAndAct
from state import TimerState, LightsState
from controllers import button_maps

config_path = './config.cfg'

if __name__ == '__main__':

    config = ConfigParser()
    config.read_file(open(config_path))

    lift_timer_window = LiftTimerWindow(config['widget_scaling'])
    lights_window = LightsWindow(config['widget_scaling'], config['light_images'])

    next_att_timer_state = TimerState()
    lift_timer_state = TimerState()

    light_state = LightsState()

    poll_act_obj = PollAndAct(config['controllers'], button_maps, next_att_timer_state, lift_timer_state, light_state, lift_timer_window, lights_window)

    # is this fine enough resolution?
    GObject.timeout_add(100, poll_act_obj.poll)

    timer_handler = TimerHandler(lift_timer_window, lights_window, next_att_timer_state, lift_timer_state)
    GObject.timeout_add(1000, timer_handler.handle_tick)

    #show lift timer initially
    lift_timer_window.show()


    Gtk.main()

