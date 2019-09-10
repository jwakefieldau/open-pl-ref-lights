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


class ControllersState(object):

    # on poll(), compare the devices present against the ones mapped if any
    # this way we can determine if any have gone away and/or if we need to 
    # (re)map

    def __init__(self):

        # key is ref position, val is InputDevice
        self.controller_dict = {}
        self.candidate_devices = []
        self.mapping_underway = False

    def begin_mapping(self, candidate_devices):

        self.candidate_devices = candidate_devices
        self.mapping_underway = True

    def end_mapping(self):

        self.candidate_devices = []
        self.mapping_underway = False

    def is_mapping(self):

        return self.mapping_underway

    def get_candidate_devices(self):

        return self.candidate_devices

    def check_controllers(self, new_input_device_list=None):

        #DEBUG
        #print('About to check to see if all controllers are mapped')

        ret = True

        #DEBUG
        #print('Currently mapped controllers: {}'.format(str(self.controller_dict)))

        if not new_input_device_list:
            new_input_device_list = self.candidate_devices

        # if we have te right number of controllers mapped, see if any have dropped off
        if len(self.controller_dict.items()) == 3:

            #NOTE - use path because phys isn't guaranteed unique (Bluetooth MAC)

            # See if any mapped controllers are missing from the newly polled list
            cur_path_set = set([input_device.path for (position, input_device,) in self.controller_dict.items()])
            new_path = set([input_device.path for input_device in new_input_device_list])

            #print('Comparing physical paths for currently mapped controllers: {} against polled input devices: {}'.format(cur_phys_set, new_phys_set))
   
            # return False if we are missing some controllers that are mapped
            if len(new_path_set.difference(cur_path_set)) > 0:
                ret = False

            # return True if all the mapped controllers are still there
            else:
                ret = True

        # return False if we haven't mapped enough controllers yet      
        else:
            ret = False

        #DEBUG
        #print('About to return {} from check_controllers()'.format(ret))

        return ret
        
    def get_controllers(self):

        return self.controller_dict

    def all_mapped(self):
  
        return (self.controller_dict.get('left') and self.controller_dict.get('head') and self.controller_dict.get('right'))

    def map_controller(self, input_device, position):

        if position in ['left', 'head', 'right']:
            self.controller_dict[position] = input_device

        else:
            raise ValueError('tried to map invalid controller position: {}'.format(position))
