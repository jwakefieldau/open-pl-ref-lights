import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from configparser import ConfigParser

from windows import LiftTimerWindow, LightsWindow

config_path = './config.cfg'

if __name__ == '__main__':

    config = ConfigParser(config_path)

    lift_timer_window = LiftTimerWindow(config['widget_scaling'])
    lights_window = LightsWindow(config['widget_scaling'])

    #show lift timer initially
    lift_timer_window.show_all()
    lift_timer_window.fullscreen()

    Gtk.main()

