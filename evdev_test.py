
# requires python3
import evdev

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
        print('detected USB gamepad, listening for events forever')
        print('-----------------------')
        break

for event in gamepad_device.read_loop():
    print(evdev.categorize(event))
        

