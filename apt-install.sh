#!/bin/bash

# from http://www.peteronion.org.uk/PyGobjectGtk+3/PyGtk.html
# internet says raspbian buster (which we should have on an rpi 4) has python 3 packaged
sudo apt-get install -y python-gi python-gi-cairo python3-gi python3-gi-cairo gir1.2-gtk-3.0 python3-evdev
mkdir -p ~/.config/autostart
cp open-pl-ref-lights.desktop ~/.config/autostart
