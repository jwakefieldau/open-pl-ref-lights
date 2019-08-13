class TimerHandler(object):

    def __init__(self):

        self.next_att_timer_state = TimerState()
        self.lift_timer_state = TimerState()

    def handle_tick(self, window, event):

        self.lift_timer_state.tick()
        self.next_att_timer_state.tick()

        #TODO - conditionally update lift timer and next att timer
        # check which window we're on 
        if hasattr(window, 'lift_timer_label'):
             #TODO - add method to TimerState to render timer str
             window.update_lift_timer(self.lift_timer_state.timer_str())
             window.show_lift_timer()

        #TODO if the next att timer has started, update and show it
