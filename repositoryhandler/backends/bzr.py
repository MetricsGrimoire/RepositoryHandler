# bzr.py
#
# Copyright (C) 2008 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
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

import re
import os

from repositoryhandler.Command import Command, CommandError
from repositoryhandler.backends import Repository, \
    RepositoryInvalidWorkingCopy, register_backend
from repositoryhandler.backends.watchers import *


def get_repository_from_path(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    pattern = re.compile("^[ \t]*(checkout of)?(parent)? branch:(.*)$")
    uri = None

    try:
        cmd = ['bzr', 'info']

        command = Command(cmd, path, env={'LC_ALL': 'C'})
        out = command.run_sync()

        for line in out.splitlines():
            match = pattern.match(line)
            if not match:
                continue

            uri = match.group(3).strip()
            break
    except CommandError:
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a Bzr '
                                           'working copy' % path)

    if uri is None:
        raise RepositoryInvalidWorkingCopy(
            '"%s" does not appear to be a Bzr'
            ' working copy' % path
        )

    return 'bzr', uri


class BzrRepository(Repository):
    '''Bazar Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'bzr')

    def _check_uri(self, uri):
        type, repo_uri = get_repository_from_path(uri)
        if not repo_uri.startswith(self.uri):
            raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a '
                                               'Bzr working copy (expected %s'
                                               ' but got %s)'
                                               % (uri, self.uri, repo_uri))

    def copy(self):
        return BzrRepository(self.uri)

    def checkout(self, module, rootdir, newdir=None, branch=None, rev=None):
        # branch doesn't make sense here module == branch
        if newdir is not None:
            srcdir = os.path.join(rootdir, newdir)
        elif newdir == '.':
            srcdir = rootdir
        else:
            srcdir = os.path.join(rootdir, module)
        if os.path.exists(srcdir):
            try:
                self.update(srcdir, rev)
                return
            except RepositoryInvalidWorkingCopy:
                # If srcdir is not a valid working copy,
                # continue with the checkout
                pass

        cmd = ['bzr', 'branch', self.uri]

        if newdir is not None:
            cmd.append(newdir)
        else:
            cmd.append(module)

        command = Command(cmd, rootdir)
        self._run_command(command, CHECKOUT)

    def update(self, uri, rev=None):
        self._check_uri(uri)

        #TODO: revision

        cmd = ['bzr', 'pull']

        if os.path.isfile(uri):
            directory = os.path.dirname(uri)
        else:
            directory = uri

        command = Command(cmd, directory)
        self._run_command(command, UPDATE)

    def log(self, uri, rev=None, files=None):
        self._check_uri(uri)

        if os.path.isfile(uri):
            cwd = os.path.dirname(uri)
            files = [os.path.basename(uri)]
        elif os.path.isdir(uri):
            cwd = uri
            files = ['.']
        else:
            cwd = os.getcwd()

        cmd = ['bzr', 'log', '-v']

        #TODO: branch

        if files is not None:
            for file in files:
                cmd.append(file)
        else:
            cmd.append(uri)

        command = Command(cmd, cwd)
        self._run_command(command, LOG)

    def rlog(self, module=None, rev=None, files=None):
        # TODO: is it supported by bzr???
        return

    def diff(self, uri, branch=None, revs=None, files=None):
        # TODO
        pass

    def blame(self, uri, rev=None, files=None):
        # TODO
        pass

    def get_modules(self):
        #Not supported by Bzr
        return []

    def get_last_revision(self, uri):
        self._check_uri(uri)

        cmd = ['bzr', 'revno']

        command = Command(cmd, uri)
        try:
            out = command.run_sync()
        except:
            return None

        if out == "":
            return None

        return out.strip('\n\t ')

register_backend('bzr', BzrRepository)
