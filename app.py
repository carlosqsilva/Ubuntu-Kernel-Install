#!/usr/bin/env python3

import gi
import os
import re
import requests
from bs4 import BeautifulSoup
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from subprocess import Popen


def available_versions(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')

    linux_versions = []
    # low latency avaiable since v3.13.2-trusty/
    get = False
    for version in soup.find_all('a'):
        href = version.get('href')
        if not get:
            if href == 'v3.13.2-trusty/':
                get = not get
            continue

        if get:
            if href.startswith('v'):
                linux_versions.append(href)

    return linux_versions


def get_filename(url, wich, arch):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')

    linux_image = re.compile(
        'linux-image-(.*)-{}_(.*)_{}.deb'.format(wich, arch))
    linux_headers = re.compile(
        'linux-headers-(.*)-{}_(.*)_{}.deb'.format(wich, arch))
    linux_all = re.compile('linux-headers-(.*)_all.deb')

    Image = Header = All = ''
    for link in soup.find_all('a'):
        search1 = re.search(linux_image, link.get_text())
        search2 = re.search(linux_headers, link.get_text())
        search3 = re.search(linux_all, link.get_text())

        if search1:
            Image = link.get('href')
        if search2:
            Header = link.get('href')
        if search3:
            All = link.get('href')

    return [url + Image, url + Header, url + All]


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
