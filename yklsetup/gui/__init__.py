#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

gui/__init__.py - Code is not needed here yet.
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
        self.window.set_default_size(700, 400)
        self.window.connect('delete-event', Gtk.main_quit)
        self.window.show_all()
        
        Gtk.main()

def main():
    app = Application()
    app.run()