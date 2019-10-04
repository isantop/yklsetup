#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

yubikey.py - Yubikey-related helper functions.
"""

import os
import subprocess

ykp_options = [
    '-y',
    '-ochal-resp',
    '-ochal-hmac',
    '-ohmac-lt64',
    '-oserial-api-visible'
]

def setup_slot(slot=2):
    ykp_command = [
        'ykpersonalize',
        f'-{slot}',
    ]
    result = subprocess.run(
        ykp_command + ykp_options, 
        capture_output=True
    )
    
    return result.returncode

def make_config(home, slot=2):
    ykp_command = [
        'ykpamcfg',
        f'-{slot}',
        '-v'
    ]
    result = subprocess.run(ykp_command, capture_output=True)
    
    try:
        initial_path = result.stdout.decode('UTF-8').split("'")[1]
        resp_filename = os.path.basename(initial_path)
    except IndexError:
        resp_filename = os.listdir(os.path.join(home, '.yubico'))[0]
        initial_path = os.path.join(home, '.yubico', resp_filename)

    resp_id = resp_filename.split('-')[-1]
    return (initial_path, resp_filename, resp_id)




