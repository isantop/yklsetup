#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

pam.py - helper functions for pam config files.
"""

import dbus
import os

bus = dbus.SystemBus()
_remote_object = bus.get_object(
    'ro.santopiet.yklsetup', '/YklsetupObject'
)

base_pam_config = 'pam_yubico.so mode=challenge-response chalresp_path=/var/yubico'
pam_files = [
    '/etc/pam.d/common-auth',
    '/etc/pam.d/login',
    '/etc/pam.d/gdm-password'
]

def get_pam_config(req='sufficient'):
    return f'auth {req} {base_pam_config}'

def modify_pam_files(req='sufficient'):
    pam_config = get_pam_config(req=req)
    for pam_file in pam_files:
        _remote_object.prepend_line(pam_file, pam_config)

