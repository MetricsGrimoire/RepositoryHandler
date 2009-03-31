# git.py
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
import re

from repositoryhandler.Command import Command, CommandError
from repositoryhandler.backends import Repository, RepositoryInvalidWorkingCopy, register_backend
from repositoryhandler.backends.watchers import *

def get_config (path, option = None):
    cmd = ['git', 'config']

    if option is not None:
        cmd.extend (['--get', option])
    else:
        cmd.extend (['-l'])

    command = Command (cmd, path, env = {'PAGER' : ''})
    out = command.run_sync ()

    if option is not None:
        return out.strip ('\n\t ')

    retval = {}
    for line in out.splitlines ():
        if '=' not in line:
            continue
        key, value = line.split ('=', 1)
        retval[key.lower ().strip ()] = value.strip ('\n\t ')

    if retval == {}:
        return None

    return retval

def get_repository_from_path (path):
    # Just in case path is a file 
    if os.path.isfile (path):
        path = os.path.dirname (path)

    try:
        uri = get_config (path, 'remote.origin.url')
    except CommandError:
        raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a Git working copy' % path)

    if uri is None or not uri:
        raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a Git working copy' % path)

    return 'git', uri
        
class GitRepository (Repository):
    '''Git Repository'''

    def __init__ (self, uri):
        Repository.__init__ (self, uri, 'git')
    
    def _check_uri (self, uri):
        type, repo_uri = get_repository_from_path (uri)
        if not repo_uri.startswith (self.uri):
            raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a Git working copy '
                                                '(expected %s but got %s)' % (uri, self.uri, repo_uri))

    def _get_branches (self, path):
        cmd = ['git', 'branch']
        
        command = Command (cmd, path)
        out = command.run_sync ()

        patt = re.compile ("^\* (.*)$")
        
        i = 0
        current = 0
        retval = []
        for line in out.splitlines ():
            if line.startswith (self.uri):
                continue

            match = patt.match (line)
            if match:
                current = i
                retval.append (match.group (1).strip (' '))
            else:
                retval.append (line.strip (' '))
            i += 1

        return current, retval
    
    def _checkout_branch (self, path, branch):
        self._check_uri (path)

        current, branches = self._get_branches (path)

        if branch in branches:
            if branches.index (branch) == current:
                return

            cmd = ['git', 'checkout', branch]
        else:
            cmd = ['git', 'checkout', '-b', branch, 'origin/%s' % (branch)]
            
        command = Command (cmd, path)
        command.run ()
        
    def checkout (self, module, rootdir, newdir = None, branch = None, rev = None):
        if newdir is not None:
            srcdir = os.path.join (rootdir, newdir)
        elif newdir == '.':
            srcdir = rootdir
        else:
            if module == '.':
                srcdir = os.path.join (rootdir, os.path.basename (self.uri.rstrip ('/')))
            else:
                srcdir = os.path.join (rootdir, module)
        if os.path.exists (srcdir):
            try:
                self.update (srcdir, rev)
                return
            except RepositoryInvalidWorkingCopy:
                # If srcdir is not a valid working copy,
                # continue with the checkout
                pass

        # module == '.' is a special case to download the whole repository
        if module == '.':
            uri = self.uri
        else:
            uri = os.path.join (self.uri, module)

        cmd = ['git', 'clone', uri]

        if newdir is not None:
            cmd.append (newdir)
        elif module == '.':
            cmd.append (os.path.basename (uri.rstrip ('/')))
        else:
            cmd.append (module)

        command = Command (cmd, rootdir)
        self._run_command (command, CHECKOUT)

        if branch is not None:
            self._checkout_branch (srcdir, branch)

    def update (self, uri, rev = None):
        self._check_uri (uri)

        branch = rev
        if branch is not None:
            self._checkout_branch (uri, branch)
        
        cmd = ['git', 'pull']

        if os.path.isfile (uri):
            directory = os.path.dirname (uri)
        else:
            directory = uri

        command = Command (cmd, directory)
        self._run_command (command, UPDATE)

    def cat (self, uri, rev = None):
        self._check_uri (uri)

        cmd = ['git', 'show']

        directory = os.path.dirname (uri)

        while not os.path.isdir (os.path.join (directory, ".git")):
            directory = os.path.dirname (directory)

        target = uri[len (directory):].strip ("/")
            
        if rev is not None:
            target = "%s:%s" % (rev, target)
        else:
            target = ":%s" % (target)

        cmd.append (target)
            
        command = Command (cmd, directory, env = {'PAGER' : ''})
        self._run_command (command, CAT)
        
    def log (self, uri, rev = None, files = None):
        self._check_uri (uri)

        if os.path.isfile (uri):
            cwd = os.path.dirname (uri)
            files = [os.path.basename (uri)]
        elif os.path.isdir (uri):
            cwd = uri
        else:
            cwd = os.getcwd ()
        
        cmd = ['git', 'log', '--all', '--topo-order', '--pretty=fuller', '--parents', '--name-status', '-M', '-C', '--decorate', 'origin']

        if rev is not None:
            cmd.append (rev)

        if files is not None:
            for file in files:
                cmd.append (file)
        elif cwd != uri:
            cmd.append (uri)

        command = Command (cmd, cwd, env = {'PAGER' : ''})
        self._run_command (command, LOG)

    def rlog (self, module = None, rev = None, files = None):
        # Not supported by Git
        return

    def diff (self, uri, branch = None, revs = None, files = None):
        # TODO
        pass

    def blame (self, uri, rev = None, files = None):
        self._check_uri (uri)

        if os.path.isfile (uri):
            cwd = os.path.dirname (uri)
            files = [os.path.basename (uri)]
        elif os.path.isdir (uri):
            cwd = uri
        else:
            cwd = os.getcwd ()

        cmd = ['git', 'blame', '--root', '-l', '-t']

        if rev is not None:
            cmd.append (rev)
        else:
            cmd.append ('origin')

        if files is not None:
            for file in files:
                cmd.append (file)
        else:
            cmd.append (uri)

        command = Command (cmd, cwd, env = {'PAGER' : ''})
        self._run_command (command, BLAME)

    def get_modules (self):
        #Not supported by Git
        return []

    def get_last_revision (self, uri):
        self._check_uri (uri)

        cmd = ['git', 'rev-list', 'HEAD^..HEAD']

        command = Command (cmd, uri, env = {'PAGER' : ''})
        try:
            out = command.run_sync ()
        except:
            return None

        if out == "":
            return None

        return out.strip ('\n\t ')

register_backend ('git', GitRepository)
