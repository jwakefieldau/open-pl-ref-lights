import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#TODO - fullscreen
window = Gtk.Window(title='Ref lights')
window.fullscreen()

#TODO - setup input devices

#TODO - get window dimensions and apply scaling to lights and font

#TEMP - demo drawing lights and next attempt submission timer
red_light = Gtk.Image()
red_light.set_from_file('redlight.png')

#TODO - config file default positions and sizes
red_light.set_position(50,50)

window.add(red_light)

#TODO - TEMP - demo drawing lift timer


window.show_all()

#TEMP - exit on keypress
window.connect('key-press-event', Gtk.main_quit)
Gtk.main()


