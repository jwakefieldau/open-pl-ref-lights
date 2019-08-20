class LightsState(object):

    def __init__(self):

        self.clear()

    def clear(self):

        self.state = {
            'left': None,
            'head': None,
            'right': None,
        }

    def is_complete(self):

        ret = False

        if [v for (k, v,) in self.state.items()].count(None) == 0:
            ret = True

        return ret

    def is_clear(self):

        ret = False

        if [v for (k, v,) in self.state.items()].count(None) == 3:
            ret = True

        return ret

    def get_state(self):

        return self.state

    def add_decision(self, position, val):

        if self.state[position] is None:
            self.state[position] = val


class TimerState(object):

   
    def __init__(self, init_seconds=60):

        self.set_seconds(init_seconds)
        self.stopped = True

    def set_seconds(self, init_seconds):

        self.cur_seconds = init_seconds

    def tick(self):

        if not self.stopped and self.cur_seconds > 0:
            self.cur_seconds -= 1

    def reset(self):

        self.set_seconds(60)

    def start(self):
     
        self.stopped = False
        
        #DEBUG
        print('started timer')

    def stop(self):
 
        self.stopped = True

        #DEBUG
        print('stopped timer')


    def is_stopped(self):

        return self.stopped

    def increment(self):

        if self.stopped:
            self.set_seconds(self.cur_seconds + 60)

    def decrement(self):

        if self.stopped:

            if self.cur_seconds - 60 < 0:
                self.set_seconds(0)

            else:
                self.set_seconds(self.cur_seconds - 60)

    def timer_str(self):

        minutes = int(self.cur_seconds / 60)
        seconds = self.cur_seconds - (minutes * 60)

        if seconds < 10:
            ret_str = '{}:0{}'.format(minutes, seconds)

        else:
            ret_str = '{}:{}'.format(minutes, seconds)

        return ret_str
