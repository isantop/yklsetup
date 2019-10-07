#!/usr/bin/python3

"""
 Copyright 2019 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

gui/headerbar.py - the GUI for yklsetup
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import yklsetup

class Headerbar(Gtk.HeaderBar):

    def __init__(self):
        Gtk.HeaderBar.__init__(self)

        self.set_show_close_button(True)
        self.set_has_subtitle(False)
        self.props.title = 'Yubikey Login'

