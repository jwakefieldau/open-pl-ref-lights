
# requires python3
import evdev

import time

device_map = {path: evdev.InputDevice(path) for path in evdev.list_devices()}

for (path, device,) in device_map.items():
    print(':{}::{}::{}:'.format(path, device.name, device.phys))
    print('-----------------------')
    print('capabilities')
    print('-----------------------')
    print(device.capabilities(verbose=True))
    print('-----------------------')

    if device.name.strip() == 'USB gamepad':
        gamepad_device = device
        print('-----------------------')
        print('detected USB gamepad, listening for events')
        print('-----------------------')
        break

#for event in gamepad_device.read_loop():
    #print(evdev.categorize(event))
        
# try reading intermittently to imitate what will happen when we run in the Gtk main loop
# do events get queued up or lost?
while True:
    print('sleeping for 5 seconds')
    time.sleep(5.0)
    print('awake!')
 
    # this throws BlockingIOError if there are no events queued up to read
    try:
        for event in gamepad_device.read():
            print(evdev.categorize(event))

    except BlockingIOError:
        pass
