# Downloader.py
#
# Copyright (C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os
from FindProgram import find_program
from Command import Command


def get_download_command(uri, dest_path, output):
    wget = find_program('wget')
    if wget is None:
        return None

    cmd = [wget, uri, '-O', dest_path, '-o', output]
    if uri.startswith('https://'):
        cmd.append('--no-check-certificate')

    return cmd


def download(uri, dirname=None, output=None):

    if dirname is None:
        dirname = os.getcwd()

    if output is None:
        output = '/dev/null'

    dest_path = os.path.join(dirname, os.path.basename(uri))
    cmd = get_download_command(uri, dest_path, output)
    if cmd is None:
        return False

    command = Command(cmd, dirname)
    try:
        command.run()
    except:
        return False

    return os.path.exists(dest_path)

if __name__ == '__main__':
    import sys

    uri = sys.argv[1]
    try:
        dir = sys.argv[2]
    except:
        dir = None
    try:
        output = sys.argv[3]
    except:
        output = None

    if download(uri, dir, output):
        print "SUSSCESS"
    else:
        print "FAILED"
