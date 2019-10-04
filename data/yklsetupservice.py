#!/usr/bin/python3

"""
 Copyright 2017-2018 Ian Santopietro <isantop@gmail.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

yklsetupservice.py - The D-Bus service that performs privileged actions
"""

import os

import gi
from gi.repository import GObject
import dbus
import dbus.service
import dbus.mainloop.glib
import time

class YklsetupException(dbus.DBusException):
    _dbus_error_name = 'ro.santopiet.yklsetup.YklsetupException'

class PermissionDeniedByPolicy(dbus.DBusException):
    _dbus_error_name = 'ro.santopiet.yklsetup.PermissionDeniedByPolicy'

class YklsetupObject(dbus.service.Object):
    def __init__(self, conn=None, object_path=None, bus_name=None):
        dbus.service.Object.__init__(self, conn, object_path, bus_name)

        # The following variables are used bu _check_polkit_privilege
        self.dbus_info = None
        self.polkit = None
        self.enforce_polkit = True
    
    @dbus.service.method(
        "ro.santopiet.yklsetup.Directories",
        in_signature='sb', out_signature='s',
        sender_keyword='sender', connection_keyword='conn'
    )
    def create_dir(self, path, executable, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, 'ro.santopiet.yklsetup.setup-yubikey'
        )

        # Set up the mode of the file
        mode = 0o600
        if executable:
            mode = 0o700
        
        try:
            os.makedirs(path, mode=mode, exist_ok=True)
        except:
            raise YklsetupException(
                f'Could not create the directory: {path}'
            )
        
        return path
    
    @dbus.service.method(
        "ro.santopiet.yklsetup.Directories",
        in_signature='s', out_signature='s',
        sender_keyword='sender', connection_keyword='conn'
    )
    def set_owner(self, path, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, 'ro.santopiet.yklsetup.setup-yubikey'
        )

        try:
            uid = os.getuid()
            gid = os.getgid()
            os.chown(path, uid, gid)
        except:
            raise YklsetupException(
                f'Could not set owner of {path} to {uid}:{gid}'
            )
        return path
    
    @dbus.service.method(
        "ro.santopiet.yklsetup.Directories",
        in_signature='ssb', out_signature='s',
        sender_keyword='sender', connection_keyword='conn'
    )
    def move_file(self, src, dest, executable, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, 'ro.santopiet.yklsetup.setup-yubikey'
        )

        mode = 0o600
        if executable:
            mode = 0o700

        try:
            os.rename(src, dest)
            os.chmod(dest, mode)
        
        except:
            raise YklsetupException(
                f'Could not set perms of file {dest} to {mode}.'
            )
        
        return dest
    
    @dbus.service.method(
        "ro.santopiet.yklsetup.Config",
        in_signature='', out_signature='',
        sender_keyword='sender', connection_keyword='conn'
    )
    def set_config(self, sender=None, conn=None):
        self._check_polkit_privilege(
            sender, conn, 'ro.santopiet.yklsetup.setup-yubikey'
        )

        inpath = '/usr/share/pam-configs/yubico-old'
        outpath = '/usr/share/pam-configs/yubico'
        try:
            os.rename(outpath, inpath)
            with open(inpath, mode='r') as infile, open(outpath, mode='x') as outfile:
                for line in infile.xreadlines():
                    outfile.write(line.replace('mode=client', 'mode=challenge-response'))
            os.remove(inpath)
        
        except:
            raise YklsetupException(
                'Could not set new configuration'
            )
    
    @dbus.service.method(
        "ro.santopiet.yklsetup.Exceptions",
        in_signature='', out_signature='',
        sender_keyword='sender', connection_keyword='conn'
    )
    def RaiseException(self, sender=None, conn=None):
        raise YklsetupException('Error setting up Yubikey')
    
    @dbus.service.method(
        "ro.santopiet.yklsetup.Operations",
        in_signature='', out_signature='',
        sender_keyword='sender', connection_keyword='conn'
    )
    def Exit(self, sender=None, conn=None):
        mainloop.quit()
    
    @classmethod
    def _log_in_file(klass, filename, string):
        date = time.asctime(time.localtime())
        ff = open(filename, "a")
        ff.write("%s : %s\n" %(date,str(string)))
        ff.close()
    
    @classmethod
    def _strip_source_line(self, source):
        source = source.replace("#", "# ")
        source = source.replace("[", "")
        source = source.replace("]", "")
        source = source.replace("'", "")
        source = source.replace("  ", " ")
        return source

    def _check_polkit_privilege(self, sender, conn, privilege):
        # from jockey
        '''Verify that sender has a given PolicyKit privilege.

        sender is the sender's (private) D-BUS name, such as ":1:42"
        (sender_keyword in @dbus.service.methods). conn is
        the dbus.Connection object (connection_keyword in
        @dbus.service.methods). privilege is the PolicyKit privilege string.

        This method returns if the caller is privileged, and otherwise throws a
        PermissionDeniedByPolicy exception.
        '''
        if sender is None and conn is None:
            # called locally, not through D-BUS
            return
        if not self.enforce_polkit:
            # that happens for testing purposes when running on the session
            # bus, and it does not make sense to restrict operations here
            return

        # get peer PID
        if self.dbus_info is None:
            self.dbus_info = dbus.Interface(conn.get_object('org.freedesktop.DBus',
                '/org/freedesktop/DBus/Bus', False), 'org.freedesktop.DBus')
        pid = self.dbus_info.GetConnectionUnixProcessID(sender)
        
        # query PolicyKit
        if self.polkit is None:
            self.polkit = dbus.Interface(dbus.SystemBus().get_object(
                'org.freedesktop.PolicyKit1',
                '/org/freedesktop/PolicyKit1/Authority', False),
                'org.freedesktop.PolicyKit1.Authority')
        try:
            # we don't need is_challenge return here, since we call with AllowUserInteraction
            (is_auth, _, details) = self.polkit.CheckAuthorization(
                    ('unix-process', {'pid': dbus.UInt32(pid, variant_level=1),
                    'start-time': dbus.UInt64(0, variant_level=1)}), 
                    privilege, {'': ''}, dbus.UInt32(1), '', timeout=600)
        except dbus.DBusException as e:
            if e._dbus_error_name == 'org.freedesktop.DBus.Error.ServiceUnknown':
                # polkitd timed out, connect again
                self.polkit = None
                return self._check_polkit_privilege(sender, conn, privilege)
            else:
                raise

        if not is_auth:
            YklsetupObject._log_in_file('/tmp/yklsetup.log','_check_polkit_privilege: sender %s on connection %s pid %i is not authorized for %s: %s' %
                    (sender, conn, pid, privilege, str(details)))
            raise PermissionDeniedByPolicy(privilege)


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SystemBus()
    name = dbus.service.BusName("ro.santopiet.yklsetup", bus)
    object = YklsetupObject(bus, '/YklsetupObject')

    mainloop = GObject.MainLoop()
    mainloop.run()