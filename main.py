import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

from configparser import ConfigParser

from windows import LiftTimerWindow, LightsWindow
from event_handlers import TimerHandler, EvdevControllerPoller
from state import TimerState
from controllers import button_maps

config_path = './config.cfg'

if __name__ == '__main__':

    config = ConfigParser(config_path)

    lift_timer_window = LiftTimerWindow(config['widget_scaling'])
    lights_window = LightsWindow(config['widget_scaling'], config['light_images'])

    next_att_timer_state = TimerState()
    lift_timer_state = TimerState()

    controller_poller = EvdevControllerPoller(config['controllers'], button_maps)
    
    #TODO - set up controller poller with add_idle

    #TODO set up timer handler
    timer_handler = TimerHandler(next_att_timer_state, lift_timer_state)
    GObject.timeout_add(1000, timer_handler.handle_tick)

    #show lift timer initially
    lift_timer_window.show()
    lift_timer_window.fullscreen()


    Gtk.main()

