
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

                    if not left_usb_path:
                        left_usb_path = dev.phys 

                    elif not head_usb_path:
                        head_usb_path = dev.phys

                    elif not right_usb_path:
                        right_usb_path = dev.phys

        except BlockingIOError:
            pass

print("left_usb_path={}".format(left_usb_path))       
print("head_usb_path={}".format(head_usb_path))       
print("right_usb_path={}".format(right_usb_path))       
    
        
