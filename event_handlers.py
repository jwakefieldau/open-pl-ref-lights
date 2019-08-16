import evdev

class TimerHandler(object):

    def __init__(self, next_att_timer_state, lift_timer_state):

        self.next_att_timer_state = next_att_timer_state
        self.lift_timer_state = lift_timer_state

    def handle_tick(self, window, event):

        self.lift_timer_state.tick()
        self.next_att_timer_state.tick()

        # check which window we're on 
        if hasattr(window, 'lift_timer_label'):
             window.update_lift_timer(self.lift_timer_state.timer_str())
             window.show_lift_timer()

        # update next att timer unconditionally
        window.update_next_att_timer(self.next_att_timer_state.timer_str())


class EvdevControllerPoller(object):

    def __init__(self, controller_config, button_maps):

        self.button_map = button_maps[controller_config['type']]

        for path in evdev.list_devices():
            cur_dev = evdev.InputDevice(path):

            if cur_dev.phys == controller_config['left_usb_path']:
                self.left_controller = cur_dev

            elif cur_dev.phys == controller_config['head_usb_path']:
                self.head_controller = cur_dev
 
            elif cur_dev.phys == controller_config['right_usb_path']:
                self.right_controller = cur_dev

    def poll(self):

        #TODO - select poll
