#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

gui.py - the GUI for yklsetup
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .headerbar import Headerbar

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.header = Headerbar()
        self.set_titlebar(self.header)

        self.content_grid = Gtk.Grid()
        self.add(self.content_grid)
        