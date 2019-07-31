import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

#TODO - fullscreen
window = Gtk.Window(title='Ref lights')
window.fullscreen()

#TODO - MARK - figure out how to do this
bg_eventbox = Gtk.EventBox()
window.add(bg_eventbox)
black_color = Gdk.Color(red=0, green=0, blue=0)
bg_eventbox.modify_bg(Gtk.StateType.NORMAL, black_color)


#TODO - setup input devices

#TODO - get window dimensions and apply scaling to lights and font
#NOTE - is this necessary given GTK layout tools?
#TODO - is a grid better
#light_grid = Gtk.Box(spacing=10)
light_grid = Gtk.Grid()
bg_eventbox.add(light_grid)

#TEMP - demo drawing lights and next attempt submission timer
left_light_pb = GdkPixbuf.Pixbuf.new_from_file('redlight.png')
left_light = Gtk.Image.new_from_pixbuf(left_light_pb.scale_simple(50, 50, GdkPixbuf.InterpType.BILINEAR))

#light_grid.pack_start(left_light, True, True, 0)
light_grid.attach(left_light, left=0, top=1, width=1, height=1)


head_light = Gtk.Image()
head_light.set_from_file('redlight.png')
#light_grid.pack_start(head_light, True, True, 0)
light_grid.attach(head_light, left=1, top=0, width=1, height=1)

right_light = Gtk.Image()
right_light.set_from_file('redlight.png')
#light_grid.pack_start(right_light, True, True, 0)
light_grid.attach(right_light, left=2, top=3, width=1, height=1)



#TODO - TEMP - demo drawing lift timer


window.show_all()

#TEMP - exit on keypress
window.connect('key-press-event', Gtk.main_quit)
Gtk.main()


