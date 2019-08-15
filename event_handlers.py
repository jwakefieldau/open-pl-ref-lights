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


class ControllerPoller(object):

    def __init__(self, left_controller, head_controller, right_controller):

        self.left_controller = left_controller
        self.head_controller = head_controller
        self.right_controller = right_controler

    #TODO - add method to run on add_idle and select etc from controllers
