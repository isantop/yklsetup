#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Portions of test-related code authored by Jason DeRose <jason@system76.com>
"""


from distutils.core import setup
from distutils.cmd import Command
import os
import subprocess
import sys

TREE = os.path.dirname(os.path.abspath(__file__))
DIRS = [
    'yklsetup',
    'bin'
]

def run_pytest():
    return run_under_same_interpreter('test', '/usr/bin/pytest-3', [])

def run_under_same_interpreter(opname, script, args):
    """Re-run with the same as current interpreter."""
    print('\n** running: {}...'.format(script), file=sys.stderr)
    if not os.access(script, os.R_OK | os.X_OK):
        print(
            'ERROR: cannot read and execute: {!r}'.format(script),
            file=sys.stderr
        )
        print(
            'Consider running `setup.py test --skip-{}`'.format(opname),
            file=sys.stderr
        )
        sys.exit(3)
    cmd = [sys.executable, script] + args
    print('check_call:', cmd, file=sys.stderr)
    try:
        subprocess.check_call(cmd)
        print('** PASSED: {}\n'.format(script), file=sys.stderr)
        return True
    except subprocess.CalledProcessError:
        print('** FAILED: {}\n'.format(script), file=sys.stderr)
        return False

def run_pyflakes3():
    """Run a round of pyflakes3."""
    script = '/usr/bin/pyflakes3'
    names = [
        'setup.py',
    ] + DIRS
    args = [os.path.join(TREE, name) for name in names]
    return run_under_same_interpreter('flakes', script, args)



class Test(Command):
    """Basic sanity checks on our code."""
    description = 'run pyflakes3'

    user_options = [
        ('skip-flakes', None, 'do not run pyflakes static checks'),
        ('skip-test', None, 'Do run run unit tests')
    ]

    def initialize_options(self):
        self.skip_sphinx = 0
        self.skip_flakes = 0
        self.skip_test = 0

    def finalize_options(self):
        pass

    def run(self):
        if not self.skip_flakes:
            pf3 = run_pyflakes3()
        if not self.skip_test:
            pt3 = run_pytest()
        if not pt3 or not pf3:
            print(
                'ERROR: One or more tests failed with errors.'
            )
            exit(3)

setup(
    name='yklsetup',
    version='0.0.2',
    author='Ian Santopietro',
    author_email='isantop@gmail.com',
    url='https://github.com/isantop/yklsetup',
    description='A simple tool to set up Yubikey login on a GNOME Desktop',
    license='ISC',
    packages=['yklsetup', 'yklsetup.gui'],
    scripts=['bin/yklsetup'],
    cmdclass={'test': Test},
    data_files = [
        ('/usr/share/dbus-1/system-services', ['data/ro.santopiet.yklsetup.service']),
        ('/usr/share/polkit-1/actions', ['data/ro.santopiet.yklsetup.policy']),
        ('/etc/dbus-1/system.d/', ['data/ro.santopiet.yklsetup.conf']),
        ('/usr/lib/yklsetup', ['data/yklsetupservice.py'])
    ]
)
