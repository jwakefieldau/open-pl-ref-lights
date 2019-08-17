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
            cur_dev = evdev.InputDevice(path):

            if cur_dev.phys == controller_config['left_usb_path']:
                self.controller_map['left'] = cur_dev

            elif cur_dev.phys == controller_config['head_usb_path']:
                self.controller_map['head'] = cur_dev
 
            elif cur_dev.phys == controller_config['right_usb_path']:
                self.controller_map['right'] = cur_dev

    def poll(self):

        for (position, dev,) in self.controller_map.items():
            try:
                controller_events = dev.read()
                
                for controller_event in controller_events:
                    #TODO - interpret and act on events using controller map based on what the state of everything is
                    #event_button = ...

                    mapped_button = self.button_map[event_button]

                    # if no ref has entered a decision, ie: we are clear, then 
                    # * head ref can start/stop the lift timer, 
                    # * head ref can reset the lift timer if it is stopped
                    # * head ref can increase or decrease the lift timer by 60 seconds if it is stopped
                    # * refs can add a ref decision if they haven't already
                    # ** then hide the lift timer window and show the lights window (but with lights hidden)

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


                    # if refs have started adding decisions, ie: we are not clear and also not complete, then
                    # * refs can add decisions if they haven't already
                    # ** if this then makes the decision complete, show the lights, and reset the next attempt timer
                    if not self.lights_state.is_complete():

                        was_clear = self.lights_state.is_clear()

                        #.add_decision() ensures a decision can only be entered from a position that was clear
                        if mapped_button == 'red_light':
                            self.lights_state.add_decision(position, False)

                        if mapped_button == 'red_light':
                            self.lights_state.add_decision(position, True)

                        if was_clear:
                            #hide lift timer window, show lights window but with lights hidden
                            self.lift_timer_window.hide()
                            self.lights_window.show()
                            #TODO - does this have the desired effect of showing the lights window but nothing in it?  Or do we need a hide_lights() method?
                            self.lights_window.hide_all()

                        if self.lights_state.is_complete():
                            #TODO - show lights and reset next attempt timer


                    # if the ref decision is complete, then
                    # * head ref can clear the lights, which then hides the lights and lights  window, shows the lift timer window
                    else:
                        #TODO

            except BlockingIOError:
                pass
