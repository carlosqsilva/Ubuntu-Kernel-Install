#! /usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup


#url = "http://kernel.ubuntu.com/~kernel-ppa/mainline/"

def avaible_versions(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'lxml')

    linux_versions = []
    #low latency avaiable since v3.13.2-trusty/
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

    linux_image = re.compile('linux-image-(.*)-{}_(.*)_{}.deb'.format(wich, arch))
    linux_headers = re.compile('linux-headers-(.*)-{}_(.*)_{}.deb'.format(wich, arch))
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

    return [url+Image, url+Header, url+All]

if __name__ == "__main__":
    print(avaible_versions(url))
