import evdev
import os
import sys

class UIHandler(object):

    def null_handler(self, widget, event):
    
        return True

class TimerHandler(object):

    def __init__(self, lift_timer_window, lights_window, next_att_timer_state, lift_timer_state):

        self.next_att_timer_state = next_att_timer_state
        self.lift_timer_state = lift_timer_state
        self.lift_timer_window = lift_timer_window
        self.lights_window = lights_window

    def handle_tick(self):

        self.lift_timer_state.tick()
        self.next_att_timer_state.tick()

        # check which window we're on by checking state of lift timer and lights windows

        if self.lift_timer_window.props.visible:

             #DEBUG
             print('timer window visible')

             self.lift_timer_window.update_lift_timer(self.lift_timer_state.timer_str())
             self.lift_timer_window.show_lift_timer()
             self.lift_timer_window.update_next_att_timer(self.next_att_timer_state.timer_str())

        elif self.lights_window.props.visible:

             #DEBUG
             print('lights window visible')

             self.lights_window.update_next_att_timer(self.next_att_timer_state.timer_str())

        #make sure we always tick again
        return True

class PollAndAct(object):

    def __init__(self, button_maps, next_att_timer_state, lift_timer_state, lights_state, controllers_state, lift_timer_window, lights_window, map_controllers_window):

        self.next_att_timer_state = next_att_timer_state
        self.lift_timer_state = lift_timer_state
        self.lights_state = lights_state
        self.controllers_state = controllers_state
        self.lift_timer_window = lift_timer_window
        self.lights_window = lights_window
        self.map_controllers_window = map_controllers_window
        self.button_maps = button_maps

    def poll_map_controllers(self):

        # maintain state of mapping operation so that we don't have to redo this every time the function
        # enters on the timer interval
        if not self.controllers_state.is_mapping():
            self.controllers_state.begin_mapping([evdev.InputDevice(path) for path in evdev.list_devices()])

        if not self.controllers_state.check_controllers():
            controller_dict = self.controllers_state.get_controllers()

            if not controller_dict.get('left'):
                cur_position = 'left'

            elif not controller_dict.get('head'):
                cur_position = 'head'    
  
            elif not controller_dict.get('right'):
                cur_position = 'right' 

            # show controller prompt
            #DEBUG
            print('About to show controller prompt for position: {}'.format(cur_position))

            self.map_controllers_window.show_controller_prompt(cur_position)

            #NOTE - return fast - we maintain state of mapping operation so
            # we don't have to poll for the list of evdev devices every time we enter
            for cur_dev in self.controllers_state.get_candidate_devices():

                try:
                    controller_events = cur_dev.read()

                    # when we have a key down event, map that input device to the current position
                    for controller_event in controller_events:
                        if controller_event.type == evdev.ecodes.EV_KEY and controller_event.value == 1:
                            self.controllers_state.map_controller(cur_dev, cur_position)

                except BlockingIOError:
                    pass


            # if all controllers are now mapped, clear the state of the mapping and show the lift timer window
            if self.controllers_state.check_controllers():
                self.controllers_state.end_mapping()
                self.map_controllers_window.hide()
                self.lift_timer_window.show()


        # make sure we fire again
        return True

	   
    def poll_controller_input(self):

        # bail if controllers aren't mapped yet
        if not self.controllers_state.all_mapped():
            return True
   
        for (position, dev,) in self.controllers_state.get_controllers().items():
            try:

                #DEBUG
                #print('Polling device {} position {}'.format(dev, position))

                controller_events = dev.read()

                for controller_event in controller_events:
                    # interpret and act on events using controller map based on what the state of everything is

                    #DEBUG
                    print(evdev.categorize(controller_event))

                    event_button = controller_event.code
                    button_map = self.button_maps[dev.name]
                    mapped_button = button_map.get(event_button)

                    # keep going on an unmapped button
                    if not mapped_button:
                        continue

                    #DEBUG
                    print('mapped event to position {} and button {}'.format(position, mapped_button))

                    #DEBUG - show state of lift timer and lights
                    print('STATE:')
                    print('lift timer stopped? {}'.format(self.lift_timer_state.is_stopped()))
                    print('lights clear? {}'.format(self.lights_state.is_clear()))
                    print('lights complete? {}'.format(self.lights_state.is_complete()))

                    # if we get a key up in the head position, check to see if we are releasing a shutdown
                    # or quit key
                    if controller_event.type == evdev.ecodes.EV_KEY and controller_event.value == 0:
                        if position == 'head':
                            
                            # if inc_timer was held the configured time, shut down
                            if mapped_button == 'inc_timer':
                                if self.controllers_state.check_shutdown_key_hold_time():

                                    #DEBUG
                                    print('About to run sudo poweroff!')

                                    os.system("sudo poweroff")

                                else:
                                    self.controllers_state.clear_shutdown_key_hold_time()

                            # if dec_timer was held the configured time, quit
                            if mapped_button == 'dec_timer':
                                if self.controllers_state.check_quit_key_hold_time():

                                    #DEBUG
                                    print('About to call sys.exit(0)!')

                                    sys.exit(0)
                                
                                else:
                                    self.controllers_state.clear_quit_key_hold_time()


                    # skip anything else that's not a key down
                    if not (controller_event.type == evdev.ecodes.EV_KEY and controller_event.value == 1):
                        continue

                    
                    # if no ref has entered a decision, ie: we are clear, then 
                    # * head ref can start/stop the lift timer, 
                    # * head ref can reset the lift timer if it is stopped
                    # * head ref can increase or decrease the lift timer by 60 seconds if it is stopped
                    # * refs can add a ref decision if they haven't already
                    # ** then hide the lift timer window and show the lights window (but with lights hidden)

                    #TODO - make this more concise, maybe write a short func or two to help

                    if self.lights_state.is_clear():
                        if position == 'head':

                            if mapped_button == 'stopstart_timer':
                                if self.lift_timer_state.is_stopped():
                                    self.lift_timer_state.start()

                                else:
                                    self.lift_timer_state.stop()

                            if mapped_button == 'reset_timer':
                                if self.lift_timer_state.is_stopped():
                                    self.lift_timer_state.reset()

                            if mapped_button == 'inc_timer':
                                if self.lift_timer_state.is_stopped():
                                    self.lift_timer_state.increment()

                            if mapped_button == 'dec_timer':
                                if self.lift_timer_state.is_stopped():
                                    self.lift_timer_state.decrement()

                        #.add_decision() ensures a decision can only be entered from a position that was clear
                        if mapped_button == 'red_light':
                            self.lights_state.add_decision(position, False)
                            #stop and reset timer, hide lift timer window, show lights window but with lights hidden
                            self.lift_timer_state.stop()
                            self.lift_timer_state.reset()
                            self.lift_timer_window.hide()
                            self.lights_window.show()
                            self.lights_window.hide_lights()

                        if mapped_button == 'white_light':
                            self.lights_state.add_decision(position, True)
                            #stop and reset timer, hide lift timer window, show lights window but with lights hidden
                            self.lift_timer_state.stop()
                            self.lift_timer_state.reset()
                            self.lift_timer_window.hide()
                            self.lights_window.show()
                            self.lights_window.hide_lights()

                    # if refs have started adding decisions, ie: we are not clear and also not complete, then
                    # * refs can add decisions if they haven't already
                    # ** if this then makes the decision complete, show the lights, and reset the next attempt timer
                    elif not self.lights_state.is_complete():

                        #.add_decision() ensures a decision can only be entered from a position that was clear
                        if mapped_button == 'red_light':
                            self.lights_state.add_decision(position, False)

                        if mapped_button == 'white_light':
                            self.lights_state.add_decision(position, True)

                        if self.lights_state.is_complete():
                            self.lights_window.show_lights(self.lights_state)
                            self.lift_timer_state.stop()
                            self.lift_timer_state.reset()
                            self.next_att_timer_state.stop()
                            self.next_att_timer_state.reset()
                            self.next_att_timer_state.start()
                            self.lights_window.show_next_att_timer()

                        else:
                            #hide lift timer window, show lights window but with lights hidden
                            self.lift_timer_window.hide()
                            self.lights_window.show()
                            self.lights_window.hide_lights()


                    # if the ref decision is complete, then
                    # * head ref can clear the lights, which then hides the lights and lights  window, and shows the lift timer window
                    else:
                        if position == 'head':
                            if mapped_button == 'clear_lights':
                                self.lights_state.clear()
                                self.lights_window.hide_lights()
                                self.lights_window.hide()
                                self.lift_timer_window.show_next_att_timer()
                                self.lift_timer_window.show()

            except BlockingIOError:
                pass


        # make sure we fire again
        return True


   

    #TODO - remove this - input polling and mapping are separate polls
    def poll(self):

        #DEBUG
        #print(datetime.datetime.now())

        new_device_list = [evdev.InputDevice(path) for path in evdev.list_devices()]

        #DEBUG
        #print('Polled device list: {}'.format(new_device_list))

        if self.controllers_state.check_controllers(new_device_list):
            self._process_controller_input()

        else:
            self._map_controllers(new_device_list)

        # make sure we fire again
        return True
