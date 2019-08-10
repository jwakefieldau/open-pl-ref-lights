import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys

class LightsApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        #TODO - windows

if __name__ == '__main__':
    app = LightsApplication()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
