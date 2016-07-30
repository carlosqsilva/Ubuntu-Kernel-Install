#!/usr/bin/env python3

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import Popen
from regulaexp import available_versions, get_filename

class app(object):
    def __init__(self):

        uname = os.uname()
        self.arch = 'amd64'
        if uname.machine != 'x86_64':
            self.arch = 'i386'

        self._url = "http://kernel.ubuntu.com/~kernel-ppa/mainline/"
        self.linux_versions = available_versions(self._url)
        self.linux_versions.reverse()

        builder = Gtk.Builder()
        builder.add_from_file("gui.glade")

        self.info = builder.get_object("info")
        self.list = builder.get_object("list_versions")
        self.what = builder.get_object("combobox")
        self.window = builder.get_object("window1")

        types = Gtk.ListStore(str)
        types.append(['Generic'])
        types.append(['Low Latency'])
        self.what.set_model(types)
        self.what.set_active(0)

        cell = Gtk.CellRendererText()
        self.what.pack_start(cell, True)
        self.what.add_attribute(cell, "text", 0)

        self.info.set_text("YOUR KERNEL\nRelease: {}\nMachine: {}".format(uname.release, self.arch))
        #for x in dir(self.what): print(x)
        for version in self.linux_versions:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(version))

            self.list.add(row)

        self.window.show_all()

        builder.connect_signals({"DeleteWindow":self.DeleteWindow, "install":self.install})

    def DeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def install(self, button):
        m = self.list.get_selected_row()
        version = self.linux_versions[m.get_index()]

        what = 'generic'
        if self.what.get_active() != 0:
            what = 'lowlatency'

        url = self._url + version
        Popen(['./terminal_intro'] + get_filename(url, what, self.arch))

if __name__ == "__main__":
	app = app()
	Gtk.main()
