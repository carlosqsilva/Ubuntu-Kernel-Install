#!/usr/bin/env python3

import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import Popen
from regulaexp import available_versions, get_filename


class app(Gtk.Window):

    _url = "http://kernel.ubuntu.com/~kernel-ppa/mainline/"

    def __init__(self, *args):
        super(app, self).__init__(*args)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_title("Ubuntu Kernel Install")
        self.set_default_size(300, 400)
        self.connect("delete-event", Gtk.main_quit)

        uname = os.uname()
        self.arch = 'amd64'
        if uname.machine != 'x86_64':
            self.arch = 'i386'

        self.linux_versions = available_versions(self._url)
        self.linux_versions.reverse()

        vbox = Gtk.VBox(spacing=6)
        # system_info = Gtk.Label(
        #     "YOUR KERNEL\tRelease: {}\nMachine: {}".format(uname.release, self.arch))
        # vbox.pack_start(system_info, False, False, 0)

        hbox = Gtk.HBox(spacing=5)
        info_label = Gtk.Label("Choose the Type of Kernel: ")

        types = Gtk.ListStore(str)
        types.append(['Generic'])
        types.append(['Low Latency'])

        self.type_combo = Gtk.ComboBox.new_with_model(types)
        renderer_text = Gtk.CellRendererText()
        self.type_combo.pack_start(renderer_text, True)
        self.type_combo.add_attribute(renderer_text, "text", 0)
        self.type_combo.set_active(0)

        hbox.pack_start(info_label, True, False, 0)
        hbox.pack_start(self.type_combo, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)

        self.listBox = Gtk.ListBox()
        self.listBox.set_activate_on_single_click(True)
        for version in self.linux_versions:
            row = Gtk.ListBoxRow()
            row.add(Gtk.Label(version))
            self.listBox.add(row)

        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.add_with_viewport(self.listBox)
        vbox.pack_start(scrolledWindow, True, True, 0)

        install_button = Gtk.Button(label="INSTALL")
        install_button.connect("clicked", self.install)
        vbox.pack_start(install_button, False, False, 0)

        self.add(vbox)
        self.show_all()

    def install(self, button):
        m = self.listBox.get_selected_row()
        version = self.linux_versions[m.get_index()]

        what = 'generic'
        if self.type_combo.get_active() != 0:
            what = 'lowlatency'

        url = self._url + version
        Popen(['./terminal_intro'] + get_filename(url, what, self.arch))

if __name__ == "__main__":
    app = app()
    Gtk.main()
