#TODO - move ths into a config file that can be written when we do the key mapping thing

button_maps = {
    'USBSNESController': {
        # map evdev key events to our common button values
        292: 'inc_timer',
        293: 'dec_timer',
        297: 'stopstart_timer',
        296: 'reset_timer',
        289: 'red_light',
        291: 'white_light',
        288: 'clear_lights',
    }
}
