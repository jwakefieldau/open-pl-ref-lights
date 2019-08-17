import evdev

button_maps = {
    'USBSNESController': {
        # map evdev key events to our common button values
        FOOBAR: 'inc_timer',
        FOOBAR: 'dec_timer',
        FOOBAR: 'stopstart_timer',
        FOOBAR: 'reset_timer',
        FOOBAR: 'red_light',
        FOOBAR: 'white_light',
        FOOBAR: 'clear_lights',
    }
}
