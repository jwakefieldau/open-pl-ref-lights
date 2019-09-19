#TODO - move ths into a config file that can be written when we do the key mapping thing

button_maps = {
    #TODO - fix this to whatever the name actually is
    'USBSNESController': {
        # map evdev key events to our common button values
        292: 'inc_timer', # R 
        293: 'dec_timer', # L 
        297: 'stopstart_timer', # start
        296: 'reset_timer', # select
        289: 'red_light', # A 
        291: 'white_light', # Y
        288: 'clear_lights', # X
    },
    '8Bitdo SN30 GamePad': {
        308: 'red_light', 
        307: 'clear_lights', 
        304: 'white_light', 
        311: 'inc_timer', 
        310: 'dec_timer', 
        314: 'reset_timer', 
        315: 'stopstart_timer'
    },
    'Logitech Pebble': {
        272: 'red_light', # left button
        273: 'white_light', # right button
    },
    'Keyboard K380': {
        27: 'inc_timer',  # close sq bracket
        26: 'dec_timer',  # open sq bracket
        15: 'stopstart_timer',  # tab
        14: 'reset_timer',  # backspace
        42: 'red_light',  # l shift
        54: 'white_light', # r shift
        57: 'clear_lights' # space
    },
}
