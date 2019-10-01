import datetime

from datetime import timedelta

import logging

log = logging.getLogger(__name__)

class LightsState(object):

    def __init__(self):

        self.clear()

    def clear(self):

        self.state = {
            'left': None,
            'head': None,
            'right': None,
        }

        log.debug('Lights cleared')

    def is_complete(self):

        ret = False

        if [v for (k, v,) in self.state.items()].count(None) == 0:
            ret = True

        log.debug('Is lights state complete? {}'.format(ret))

        return ret

    def is_clear(self):

        ret = False

        if [v for (k, v,) in self.state.items()].count(None) == 3:
            ret = True
        
        log.debug('Is lights state clear? {}'.format(ret))

        return ret

    def get_state(self):

        log.debug('About to return lights state: {}'.format(str(self.state)))

        return self.state

    def add_decision(self, position, val):

        if self.state[position] is None:
            self.state[position] = val

        log.debug('Added decision {} to position {}'.format(val, position))


class TimerState(object):

   
    def __init__(self, init_seconds=60):

        self.set_seconds(init_seconds)
        self.init_seconds = init_seconds
        self.stopped = True

    def set_seconds(self, init_seconds):

        self.cur_seconds = init_seconds

        log.debug('Set timer to {} seconds'.format(self.cur_seconds))

    def tick(self):

        if not self.stopped and self.cur_seconds > 0:
            self.cur_seconds -= 1

    def reset(self):

        self.set_seconds(self.init_seconds)

        log.debug('Reset timer')

    def start(self):
     
        self.stopped = False
        
        log.debug('started timer')

    def stop(self):
 
        self.stopped = True

        log.debug('stopped timer')


    def is_stopped(self):

        log.debug('Is timer stopped? {}'.format(self.stopped))

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

    def __init__(self, controller_config_dict):

        # key is ref position, val is InputDevice
        self.controller_dict = {}
        self.candidate_devices = []
        self.mapping_underway = False
        self.mapping_start_dt = None
        self.mapping_timeout = int(controller_config_dict['mapping_timeout'])
        self.exit_key_hold_time = int(controller_config_dict['exit_key_hold_time'])
        self.quit_key_hold_dt = None
        self.shutdown_key_hold_dt = None


    def begin_mapping(self, candidate_devices):

        self.candidate_devices = candidate_devices
        self.mapping_underway = True
        self.mapping_start_dt = datetime.datetime.utcnow()

        log.debug('Started controller device mapping with devices: {}'.format(str(self.candidate_devices)))

    def end_mapping(self):

        self.candidate_devices = []
        self.mapping_underway = False
        self.mapping_start_dt = None

        log.debug('Finished controller device mapping')

    def is_mapping(self):

        return self.mapping_underway

    def is_mapping_timed_out(self):

        now_dt = datetime.datetime.utcnow()
        ret = False

        log.debug('Comparing current time {} against mapping start time {}'.format(now_dt, self.mapping_start_dt))

        if (now_dt - self.mapping_start_dt) > timedelta(seconds=self.mapping_timeout):
            log.debug('Mapping operation timed out')
            ret = True

        return ret

    def get_candidate_devices(self):

        return self.candidate_devices

    def check_controllers(self, new_input_device_list=None):

        ret = True

        if not new_input_device_list:
            new_input_device_list = self.candidate_devices

        # if we have te right number of controllers mapped, see if any have dropped off
        if len(self.controller_dict.items()) == 3:

            #NOTE - use path because phys isn't guaranteed unique (Bluetooth MAC)

            # See if any mapped controllers are missing from the newly polled list

            # InputDevice.path appears to now be .fn for some reason

            cur_path_set = set([input_device.fn for (position, input_device,) in self.controller_dict.items()])
            new_path_set = set([input_device.fn for input_device in new_input_device_list])

            log.debug('Comparing physical paths for currently mapped controllers: {} against polled input devices: {}'.format(cur_path_set, new_path_set))
   
            # return False if we are missing some controllers that are mapped
            if len(cur_path_set.difference(new_path_set)) > 0:

                log.debug('Difference in controller mapping: {}, mapped set: {}, polled set: {}'.format(new_path_set.difference(cur_path_set), cur_path_set, new_path_set))
                ret = False

            # return True if all the mapped controllers are still there
            else:
                ret = True

        # return False if we haven't mapped enough controllers yet      
        else:
            ret = False

        log.debug('About to return {} from check_controllers()'.format(ret))

        return ret
        
    def get_controllers(self):

        return self.controller_dict

    def all_mapped(self):
  
        return (self.controller_dict.get('left') and self.controller_dict.get('head') and self.controller_dict.get('right'))

    def map_controller(self, input_device, position):

        if position in ['left', 'head', 'right']:
            self.controller_dict[position] = input_device

            log.info('Assigned controller {} to position {}'.format(input_device, position))

        else:
            raise ValueError('tried to map invalid controller position: {}'.format(position))


    def start_quit_key_hold(self):

        if not self.quit_key_hold_dt:
            self.quit_key_hold_dt = datetime.datetime.utcnow()

    def start_shutdown_key_hold(self):
        
        if not self.shutdown_key_hold_dt:
            self.shutdown_key_hold_dt = datetime.datetime.utcnow()

    def check_quit_key_hold_time(self):

        now_dt = datetime.datetime.utcnow()
        ret = False

        log.debug('About to check current time {} against quit key down time {} and configured hold time {}'.format(now_dt, self.quit_key_hold_dt, self.exit_key_hold_time))

        if self.quit_key_hold_dt:
            if (datetime.datetime.utcnow() - self.quit_key_hold_dt) >= timedelta(seconds=self.exit_key_hold_time):
                ret = True

        return ret
        
    def check_shutdown_key_hold_time(self):
        
        now_dt = datetime.datetime.utcnow()
        ret = False

        log.debug('About to check current time {} against shutdown key down time {} and configured hold time {}'.format(now_dt, self.shutdown_key_hold_dt, self.exit_key_hold_time))


        if self.shutdown_key_hold_dt:
            if (datetime.datetime.utcnow() - self.shutdown_key_hold_dt) >= timedelta(seconds=self.exit_key_hold_time):
                ret = True

        return ret
 
    def clear_quit_key_hold_time(self):

        self.quit_key_hold_dt = None

    def clear_shutdown_key_hold_time(self):

        self.shutdown_key_hold_dt = None

