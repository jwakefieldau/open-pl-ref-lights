import evdev

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

             self.lift_timer_window.update_next_att_timer(self.next_att_timer_state.timer_str())

        #make sure we always tick again
        return True

class PollAndAct(object):

    def __init__(self, controller_config, button_maps, next_att_timer_state, lift_timer_state, lights_state, lift_timer_window, lights_window):

        self.button_map = button_maps[controller_config['type']]
        self.controller_map = {}
        self.next_att_timer_state = next_att_timer_state
        self.lift_timer_state = lift_timer_state
        self.lights_state = lights_state
        self.lift_timer_window = lift_timer_window
        self.lights_window = lights_window

        for path in evdev.list_devices():
            cur_dev = evdev.InputDevice(path)

            if cur_dev.phys == controller_config['left_usb_path']:
                self.controller_map['left'] = cur_dev

                #DEBUG
                print('mapped phys {} to left position'.format(cur_dev.phys))

            elif cur_dev.phys == controller_config['head_usb_path']:
                self.controller_map['head'] = cur_dev

                #DEBUG
                print('mapped phys {} to head position'.format(cur_dev.phys))

 
            elif cur_dev.phys == controller_config['right_usb_path']:
                self.controller_map['right'] = cur_dev

                #DEBUG
                print('mapped phys {} to right position'.format(cur_dev.phys))


    def poll(self):

        for (position, dev,) in self.controller_map.items():
            try:

                #DEBUG
                #print('Polling device {} position {}'.format(dev, position))

                controller_events = dev.read()

                for controller_event in controller_events:
                    # interpret and act on events using controller map based on what the state of everything is

                    #DEBUG
                    print(evdev.categorize(controller_event))

                    # skip anything that's not a key down
                    if not (controller_event.type == evdev.ecodes.EV_KEY and controller_event.value == 1):
                        continue

                    event_button = controller_event.code
                    mapped_button = self.button_map[event_button]

                    #DEBUG
                    print('mapped event to position {} and button {}'.format(position, mapped_button))

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
                            self.next_att_timer_state.reset()
                            self.next_att_timer_state.start()

                        else:
                            #hide lift timer window, show lights window but with lights hidden
                            self.lift_timer_window.hide()
                            self.lights_window.show()
                            self.lights_window.hide_lights()


                    # if the ref decision is complete, then
                    # * head ref can clear the lights, which then hides the lights and lights  window, shows the lift timer window
                    else:
                        if position == 'head':
                            if mapped_button == 'clear_lights':
                                self.lights_window.hide_lights()
                                self.lights_window.hide()
                                self.lift_timer_window.show()
                                self.lift_timer_state.reset()
                                self.lift_timer_state.start()

            except BlockingIOError:
                pass

        #DEBUG
        #print('done polling controllers')
           
        # make sure we run again
        return True
