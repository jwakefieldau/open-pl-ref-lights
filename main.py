import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

import datetime

def timer_tick(label_widget, span_size,  start_dt, max_timer_seconds=60, prefix_str=''):

    # return true to fire again
    ret = False

    cur_dt = datetime.datetime.now()
    timer_td = cur_dt - start_dt
    timer_total_countdown_seconds = int(max_timer_seconds - timer_td.seconds)

    # don't let it go negative
    if timer_total_countdown_seconds > 0:
        timer_min = int(timer_total_countdown_seconds / 60)
        timer_sec = timer_total_countdown_seconds - (timer_min * 60)

        ret = True
    
    else:
        timer_min = 0
        timer_sec = 0

    # pad seconds with leading zeroes
    if timer_sec < 10:
        timer_sec_str = '0{}'.format(timer_sec)
    
    else:
        timer_sec_str = str(timer_sec)   

    label_widget.set_markup('<span size="{}" foreground="white">{} {}:{}</span>'.format(span_size, prefix_str, timer_min, timer_sec_str))

    return ret


def handle_key_press(window, event):

    #TODO - actually do input control, for now just toggle lift timer and lights
    if event.keyval == ord('f'):
        lift_timer_window.hide()
        light_window.show_all()

    if event.keyval == ord('j'):
        light_window.hide()
        lift_timer_window.show_all()

    if event.keyval == ord('x'):
        Gtk.main_quit()


#TODO - make this actually do something - mockup
lift_timer_window = Gtk.Window(title='Lift Timer')
lift_timer_window.fullscreen()

lift_timer_bg_eventbox = Gtk.EventBox()
lift_timer_window.add(lift_timer_bg_eventbox)

black_color = Gdk.Color(red=0, green=0, blue=0)
lift_timer_bg_eventbox.modify_bg(Gtk.StateType.NORMAL, black_color)

lift_timer_label = Gtk.Label()
lift_timer_bg_eventbox.add(lift_timer_label)

#TODO - ue scaling on span size
lift_timer_label.set_markup('<span size="240000" foreground="white">01:00</span>')

lift_timer_window.show_all()

light_window = Gtk.Window(title='Ref lights')
light_window.fullscreen()

bg_eventbox = Gtk.EventBox()
light_window.add(bg_eventbox)
vbox = Gtk.VBox(False, 4)
bg_eventbox.add(vbox)
black_color = Gdk.Color(red=0, green=0, blue=0)
bg_eventbox.modify_bg(Gtk.StateType.NORMAL, black_color)


#TODO - setup input devices

screen = light_window.get_screen()
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
GObject.timeout_add(1000, timer_tick, next_att_timer_label, next_att_timer_label_size, next_att_timer_start_dt, 60, 'Next attempt submission:')

#TEMP - exit on keypress
lift_timer_window.connect('key-press-event', handle_key_press)
light_window.connect('key-press-event', handle_key_press)

Gtk.main()




