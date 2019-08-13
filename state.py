class LightsState(object):

    def __init__(self):

        self.clear()

    def clear(self):

        self.left = None
        self.head = None
        self.right = None

class TimerState(object):

    default_init_seconds = 60
    default_increment_seconds = 60
   
    def __init__(self, init_seconds=LiftTimerState.default_init_seconds):

        self.set_seconds(init_seconds)
        self.stopped = True

    def set_seconds(self, init_seconds):

        self.cur_seconds = init_seconds

    def tick(self):

        if not self.stopped and self.cur_seconds > 0:
            self.cur_seconds -= 1

    def reset(self):

        self.set_seconds(LiftTimerState.default_init_seconds)

    def start(self):
 
        self.stopped = False

    def stop(self):
 
        self.stopped = True

    def increment(self):

        if self.stopped:
            self.set_seconds(self.cur_seconds + LiftTimerState.default_increment_seconds)

    def decrement(self):

        if self.stopped:

            if self.cur_seconds - LiftTimerState.default_increment_seconds < 0:
                self.set_seconds(0)

            else:
                self.set_seconds(self.cur_seconds - LiftTimerState.default_increment_seconds)

    def timer_str(self):

        minutes = int(self.cur_seconds / 60)
        seconds = self.cur_seconds - (minutes * 60)

        if seconds < 10:
            ret_str = '{}:0{}'.format(minutes, seconds)

        else:
            ret_str = '{}:{}'.format(minutes, seconds)

        return ret_str
