#TODO - move ths into a config file that can be written when we do the key mapping thing

button_maps = {
    #TODO - fix this to whatever the name actually is
    'USBSNESController': {
        # map evdev key events to our common button values
        292: 'inc_timer',
        293: 'dec_timer',
        297: 'stopstart_timer',
        296: 'reset_timer',
        289: 'red_light',
        291: 'white_light',
        288: 'clear_lights',
    },
    '8Bitdo SN30 GamePad': {
        304: 'red_light', 
        307: 'clear_lights', 
        308: 'white_light', 
        310: 'inc_timer', 
        311: 'dec_timer', 
        314: 'reset_timer', 
        315: 'stopstart_timer'
    },
    'Logitech Pebble': {
        272: 'red_light',
        273: 'white_light',
    },
    #TODO - Logitech K380 keyboard
}
