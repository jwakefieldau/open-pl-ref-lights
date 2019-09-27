# User Manual

This assumes the use of 8BitDo SN30 Bluetooth controllers, on a system that has been set up ready for delivery, with the controllers already paired.

## Requirements

* A HDMI display 
* Mains power outlets for the system and the display
* Referees

## Supplied

* Computer 
* Power supply - **only** use this power supply, as it is guaranteed to provide the correct level of current
* HDMI cable
* 3x controllers

The current hardware platform is a RaspberryPi 4, with a mains to USB-C power supply, micro-HDMI-to-HDMI cable,
and on-board Bluetooth receiver.

## Startup / setup

1. Turn on the display.
1. Connect the computer to the display.
1. Connect the computer to the mains power, it should power on immediately, boot within seconds and start the ref lights software automatically.
1. Turn on the controllers - on each, press the START button and the blue LED on top should flash briefly and then go solid.
1. Press any button on the left, head, and right controllers, as prompted by the software.  This allows the software to identify which referee position the input is coming from.
    1. **NOTE** the controllers will automatically power off if left idle for long enough.  If this happens, the software will detect that controllers are missing and again prompt to map the controllers for each referee position.
1. You should now see the lift timer on the display.

## In-meet operation / controls

### Head referee only

* START - start/stop the lift timer
* SELECT - reset the lift timer to 1:00
* R (the right button on the top of the controller) - add a minute to the lift timer
** this is handy for eg: setting a 10 minute timer between squat and bench press
** hold down this button for 10 seconds or more and release to shut down the system
* L (the left button on the top of the controller) - subtract a minute from the lift timer
** hold down this button for 10 seconds or more to exit the software (only useful for debugging purposes)
* X - clear lights and return to lift timer

**NOTE**:
* The software does not mandate operation of the lift timer.  If the meet does not require it, referees may simply enter a decision without the lift timer having been started.
* As soon as the decision is complete (ie: a decision has been entered by all three referees and the lights displayed), the one minute timer for the lifter to submit their next attempt will start.

### All referees

* Y - red light
* A - white light

**NOTE**:
* As soon as the first referee has entered a decision, the lift timer will disappear.  When all three referees have entered a decision, the lights will display and the next attempt submission timer will start.

## Shutdown (IMPORTANT)

When the meet is over, shut down the lights system by holding down the R button for more than 10 seconds and then releasing.  This tells the lights software to shutdown the underlying operating system cleanly.  **Please do this rather than simply disconnecting the mains power**.  Once the system is shut down, the display will indicate that there is no video signal.
