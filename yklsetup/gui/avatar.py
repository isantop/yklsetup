
"""
 Copyright 2019 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

gui/avatar.py - the GUI for yklsetup
"""

import os

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import yklsetup

class UserImage(Gtk.Image):
    def __init__(self, parent):
        Gtk.Image.__init__(self, parent)

        self.username = yklsetup.system.get_username()
        user_avatar_path = os.path.join(
            '/var/lib/AccountsService/icons',
            self.username
        )

        self.image = cairo.ImageSurface.create_from_png(
            user_avatar_path
        )
        width = self.image.get_width()
        height = self.image.get_height()

