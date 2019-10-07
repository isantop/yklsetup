#!/usr/bin/python3

"""
 Copyright 2019 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

gui/main.py - the GUI for yklsetup
"""

import logging
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from .window import Window

class Application(Gtk.Application):

    def do_activate(self):
        self.log = logging.getLogger('yklsetup.gui')
        self.window = Window()
        self.window.set_default_size(400, 300)
        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        
        Gtk.main()

