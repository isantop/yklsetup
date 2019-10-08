
"""
 Copyright 2019 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

gui/avatar.py - the GUI for yklsetup
"""

import math
import os

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import yklsetup

class UserImage(Gtk.Image):
    def __init__(self, parent):
        Gtk.Image.__init__(self, parent)
    
        self.surface = cairo.Image.surface(cairo.Format.ARGB32, 96, 96)
        self.context = cairo.Context(self.surface)

        self.context.arc(96, 96, 48, 0, 2 * math.pi)
        self.context.clip()
        self.context.new_path()

        
