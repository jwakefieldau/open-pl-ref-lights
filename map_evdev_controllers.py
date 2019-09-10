
import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

for dev in devices:
    print(dev)

left_usb_path = None
head_usb_path = None
right_usb_path = None

left_msg = False
head_msg = False
right_msg = False

while (not left_usb_path) or (not head_usb_path) or (not right_usb_path):

    for dev in devices:

        if not left_usb_path and not left_msg:
            print('Press a button on the LEFT controller')
            left_msg = True
       
        elif left_usb_path and not head_usb_path and not head_msg:
            print('Press a button on the HEAD controller')
            head_msg = True
   
        elif left_usb_path and head_usb_path and not right_usb_path and not right_msg:
            print('Press a button on the RIGHT controller')
            right_msg = True
        
        try:
            for event in dev.read():
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:

                    print('got key event code: {}'.format(event.code))

                    if not left_usb_path:
                        left_usb_path = dev.phys 

                    elif not head_usb_path:
                        head_usb_path = dev.phys
                        head_dev = dev

                    elif not right_usb_path:
                        right_usb_path = dev.phys

        except BlockingIOError:
            pass

# get button map for head controller since all controllers should be the same and head uses all buttons

button_map = {}

key_names = [
    'inc_timer',
    'dec_timer',
    'stopstart_timer',
    'reset_timer',
    'red_light',
    'white_light',
    'clear_lights',
]

for key_name in key_names:

    print('Press the {} button on the HEAD controller'.format(key_name))

    got_button = False

    while not got_button:

        try:
            for event in head_dev.read():
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                    button_map[event.code] = key_name
                    got_button = True

        except BlockingIOError:
             pass         
 
super_button_map = {head_dev.name: button_map}

print("left_usb_path={}".format(left_usb_path))       
print("head_usb_path={}".format(head_usb_path))       
print("right_usb_path={}".format(right_usb_path))       
        
print(super_button_map)
