import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

import datetime

def next_att_timer_tick(label_widget, span_size,  start_dt):
    cur_dt = datetime.datetime.now()
    timer_td = cur_dt - start_dt
    timer_total_countdown_seconds = int(60 - timer_td.seconds)

    # don't let it go negative
    if timer_total_countdown_seconds > 0:
        timer_min = int(timer_total_countdown_seconds / 60)
        timer_sec = timer_total_countdown_seconds - (timer_min * 60)
    
    else:
        timer_min = 0
        timer_sec = 0

    label_widget.set_markup('<span size="{}" foreground="white">Next attempt submission: {}:{}</span>'.format(span_size, timer_min, timer_sec))

window = Gtk.Window(title='Ref lights')
window.fullscreen()

bg_eventbox = Gtk.EventBox()
window.add(bg_eventbox)
vbox = Gtk.VBox(False, 4)
bg_eventbox.add(vbox)
black_color = Gdk.Color(red=0, green=0, blue=0)
bg_eventbox.modify_bg(Gtk.StateType.NORMAL, black_color)


#TODO - setup input devices

#TODO - get window dimensions and apply scaling to lights and font
screen = window.get_screen()
screen_width = screen.width()
screen_height = screen.height()

# scale lights based on smaller dimension
if screen_width < screen_height:
    light_width = screen_width * 0.30
    light_height = light_width

else:
    light_height = screen_height * 0.30
    light_width = light_height
    
col_spacing = screen_width * 0.03
next_att_timer_label_size = int(screen_height * 0.05) * 1000

#NOTE - is this necessary given GTK layout tools?
#TODO - is a grid better
light_box = Gtk.Box(spacing=col_spacing)
vbox.pack_start(light_box, True, True, 0)

#light_grid = Gtk.Grid()
#bg_eventbox.add(light_grid)

#light_grid.set_column_spacing(col_spacing)

#TEMP - demo drawing lights and next attempt submission timer
left_light_pb = GdkPixbuf.Pixbuf.new_from_file('redlight.png')
left_light = Gtk.Image.new_from_pixbuf(left_light_pb.scale_simple(light_width, light_height, GdkPixbuf.InterpType.BILINEAR))

light_box.pack_start(left_light, True, True, 0)
#light_grid.attach(left_light, left=0, top=1, width=1, height=1)

head_light_pb = GdkPixbuf.Pixbuf.new_from_file('redlight.png')
head_light = Gtk.Image.new_from_pixbuf(head_light_pb.scale_simple(light_width, light_height, GdkPixbuf.InterpType.BILINEAR))

light_box.pack_start(head_light, True, True, 0)
#light_grid.attach(head_light, left=1, top=1, width=1, height=1)

right_light_pb = GdkPixbuf.Pixbuf.new_from_file('redlight.png')
right_light = Gtk.Image.new_from_pixbuf(right_light_pb.scale_simple(light_width, light_height, GdkPixbuf.InterpType.BILINEAR))

light_box.pack_start(right_light, True, True, 0)
#light_grid.attach(right_light, left=2, top=1, width=1, height=1)

# demo next attempt timer
next_att_timer_label = Gtk.Label()
next_att_timer_label.set_markup('<span size="{}" foreground="white">Next attempt submission: 00:50</span>'.format(next_att_timer_label_size))

#light_grid.attach(next_att_timer_label, left=0, top=2, width=3, height=1)
next_att_timer_box = Gtk.Box()
vbox.pack_start(next_att_timer_box, True, True, 0)
next_att_timer_box.pack_end(next_att_timer_label, True, True, 0)

#set timer callback
next_att_timer_start_dt = datetime.datetime.now()
GObject.timeout_add(1000, next_att_timer_tick, next_att_timer_label, next_att_timer_label_size, next_att_timer_start_dt)

#TODO - TEMP - demo drawing lift timer

window.show_all()

#TEMP - exit on keypress
window.connect('key-press-event', Gtk.main_quit)
Gtk.main()




