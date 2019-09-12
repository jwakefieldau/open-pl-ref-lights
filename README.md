# open-pl-ref-lights
Powerlifting lights and timer system, Python based.  Output is a monitor/TV, input is from USB or Bluetooth devices such as gamepads or numpad keyboards.  Intended to run on a RaspberryPi

## current issues
* change polling class to find button map based on name reported in evdev device list rather than config so we can do mice for side refs and keyboard for head ref
* add logic to quit eg: ctrl+c
* add something to do auto pairing and connection for devices matching certain criteria
** or not?  If we add a clean quit option then pairing can be done via keyboard
** this should be a fairly unusual event
* test with bluetooth mice for sides and bluetooth keyboard for head
** block tracking sensor for mice
* test with IR numpad keyboards?
* don't forget to script or at least document setup
** auto-login as user that runs this
** auto-start this app
** user that runs this should be in the `input` group so that we can map extra keyboards
* add "cheat codes" to re-map controllers, do button mapping for unrecognised controllers
* do we need to show something other than a blank screen when the decision is incomplete?
* maybe make button handling / decision logic more concise?  can it be?
* add proper debug logging instead of prints
* test as much as possible
