import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#TODO - fullscreen
window = Gtk.Window(title='Ref lights')
window.fullscreen()

#TODO - MARK - figure out how to do this
window.modify_bg(Gtk.STATE_NORMAL, Gtk.gdk.Color('#000000'))

#TODO - setup input devices

#TODO - get window dimensions and apply scaling to lights and font
#NOTE - is this necessary given GTK layout tools?
#TODO - is a grid better
light_box = Gtk.Box(spacing=10)
window.add(light_box)

#TEMP - demo drawing lights and next attempt submission timer
left_light = Gtk.Image()
left_light.set_from_file('redlight.png')

light_box.pack_start(left_light, True, True, 0)

head_light = Gtk.Image()
head_light.set_from_file('redlight.png')
light_box.pack_start(head_light, True, True, 0)

right_light = Gtk.Image()
right_light.set_from_file('redlight.png')
light_box.pack_start(right_light, True, True, 0)


#TODO - TEMP - demo drawing lift timer


window.show_all()

#TEMP - exit on keypress
window.connect('key-press-event', Gtk.main_quit)
Gtk.main()


