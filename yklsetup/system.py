#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

system.py - A small system interface module
"""

import dbus
import os
import pwd
import sys

bus = dbus.SystemBus()
_remote_object = bus.get_object(
    'ro.santopiet.yklsetup', '/YklsetupObject'
)

def ensure_sys_config_dir(path='/var/yubico'):
    try:
        created_path = _remote_object.create_dir(path, True)
        _remote_object.set_owner(path)
    except:
        exc = sys.exc_info()
        raise exc

    return created_path

def get_username():
    return pwd.getpwuid(os.getuid()).pw_name

def get_user_home():
    return os.path.expanduser('~')

def privilged_move_file(src, dest, executable=False):
    try:
        moved_file = _remote_object.move_file(src, dest, executable)
    except:
        exc = sys.exc_info()
        raise exc

    return moved_file

def privilged_delete_file(path):
    _remote_object.remove_file(path)

def quit_service():
    _remote_object.Exit()

def restart_service():
    global _remote_object
    _remote_object.Exit()
    _remote_object = bus.get_object(
        'ro.santopiet.yklsetup', '/YklsetupObject'
    )

def get_auths():
    return _remote_object.list_auths()

def deauthorize_yuibikey():
    auths = get_auths()
    
    for auth in auths:
        if get_username() in auth:
            path = os.path.join('/var/yubico', auth)
            _remote_object.remove_file(path)
