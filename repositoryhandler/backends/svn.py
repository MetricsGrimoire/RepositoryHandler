# svn.py
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

from repositoryhandler.Command import Command, CommandError
from repositoryhandler.backends import (Repository, RepositoryInvalidWorkingCopy,
                                        RepositoryInvalidBranch, register_backend)
from repositoryhandler.backends.watchers import *

def get_info (uri):
    if os.path.isdir (uri):
        path = uri
        uri = '.'
    else:
        path = '.'
        
    cmd = ['svn', 'info', uri]

    command = Command (cmd, path, env = {'LC_ALL' : 'C'})
    out = command.run_sync ('p\n')

    retval = {}
    for line in out.splitlines ():
        if ':' not in line:
            continue
        key, value = line.split (':', 1)
        retval[key.lower ().strip ()] = value.strip ()

    if retval == {} or (retval.has_key (uri) and retval[uri] == '(Not a valid URL)'):
        return None
        
    return retval

def list_files (uri):
    if os.path.isdir (uri):
        path = uri
        uri = '.'
    else:
        path = '.'

    cmd = ['svn', 'ls', uri]

    command = Command (cmd, path, env = {'LC_ALL' : 'C'})
    out = command.run_sync ()

    retval = []
    for line in out.splitlines ():
        retval.append (line.strip ())
        
    return retval

def get_repository_from_path (path):
    # Just in case path is a file
    if os.path.isfile (path):
        path = os.path.dirname (path)
        
    try:        
        info = get_info (path)
    except CommandError:
        raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a SVN working copy' % path)

    if info is None:
        raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a SVN working copy' % path)

    return 'svn', info['repository root']

class SVNRepository (Repository):
    '''SVN Repository'''

    def __init__ (self, uri):
        try:
            info = get_info (uri)
            root = info['repository root']
        except:
            root = uri
            
        Repository.__init__ (self, root, 'svn')

    def _check_uri (self, uri):
        def is_local (uri):
            import re
            return re.compile ("^.*://.*$").match (uri) is None

        if is_local (uri):
            type, repo_uri = get_repository_from_path (uri)
            if repo_uri != self.uri:
                raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a SVN working copy '
                                                    '(expected %s but got %s)' % (uri, self.uri, repo_uri))
        else:
            if not uri.startswith (self.uri):
                raise RepositoryInvalidWorkingCopy ('"%s" does not appear to be a SVN working copy '
                                                    'for repository %s' % (uri, self.uri))

    def __get_uri_for_branch (self, module, branch):
        if branch is None:
            uri = os.path.join (self.uri, module)
        elif branch == 'trunk':
            uri = os.path.join (self.uri, 'trunk')
        else:
            uri = os.path.join (self.uri, 'branches', branch)

        try:
            info = get_info (uri)
            if info is not None:
                return uri
        except CommandError:
            raise RepositoryInvalidBranch ('Invalid branch name "%s" for repository %s' % (branch, self.uri))
        
        return uri

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
            uri = self.__get_uri_for_branch (module, branch)
        
        cmd = ['svn', 'checkout', uri]

        if newdir is not None:
            cmd.append (newdir)
        elif module == '.':
            cmd.append (os.path.basename (uri.rstrip ('/')))
        else:
            cmd.append (module)

        if rev is not None:
            cmd.extend (['-r', rev])

        command = Command (cmd, rootdir)
        self._run_command (command, CHECKOUT)

    def update (self, uri, rev = None, force = False):
        if not force:
            self._check_uri (uri)

        cmd = ['svn', 'update']

        if rev is not None:
            cmd.extend (['-r', rev])
        
        cmd.append (uri)
        command = Command (cmd)
        self._run_command (command, UPDATE)

    def log (self, uri, rev = None, files = None):
        self._check_uri (uri)

        if os.path.isfile (uri):
            cwd = os.path.dirname (uri)
            target = '.'
        elif os.path.isdir (uri):
            cwd = uri
            target = '.'
        else:
            cwd = os.getcwd ()
            target = uri

        cmd = ['svn', '-v', 'log']

        if rev is not None:
            cmd.extend (['-r', rev])

        if files is not None:
            if target != '.':
                cmd.append (target)
                
            for file in files:
                cmd.append (file)
        else:
            cmd.append (target)

        command = Command (cmd, cwd, env = {'LC_ALL' : 'C'})
        self._run_command (command, LOG)

    def diff (self, uri, branch = None, revs = None, files = None):
        self._check_uri (uri)

        if os.path.isfile (uri):
            cwd = os.path.dirname (uri)
            target = '.'
        elif os.path.isdir (uri):
            cwd = uri
            target = '.'
        else:
            cwd = os.getcwd ()

        if uri.startswith (self.uri):
            # Remote URI
            if uri.find ('trunk') >= 0 or uri.find ('branches') >= 0:
                target = uri
            else:
                if branch is not None:
                    target = os.path.join (uri, 'branches', branch)
                else:
                    target = os.path.join (uri, 'trunk')

        cmd = ['svn', 'diff']

        if revs is not None:
            if len (revs) == 1:
                cmd.extend (['-r', revs[0]])
            elif len (revs) > 1:
                cmd.extend (['-r', revs[0] + ':' + revs[1]])

        if files is not None:
            for file in files:
                if target == '.':
                    cmd.append (file)
                else:
                    cmd.append (os.path.join (target, file))
        else:
            cmd.append (target)

        command = Command (cmd, cwd, env = {'LC_ALL' : 'C'})
        self._run_command (command, DIFF)

    def get_modules (self):
        # Two 'standard' repository layouts
        # repo/trunk repo/branches
        #
        # repo/project1/trunk repo/project1/branches
        # repo/project2/trunk repo/project2/branches
        #
        # See Version Control with Subversion, page 98
        #

        # Try the first layout
        uri = os.path.join (self.uri, 'trunk')
        try:
            info = get_info (uri)
            if info is not None:
                return [self.uri.split ('/')[-1]]
        except CommandError:
            # Try with the other layout
            pass

        # Second layout
        retval = []
        modules = list_files (self.uri)
        for module in modules:
            uri = os.path.join (self.uri, module, 'trunk')

            try:
                info = get_info (uri)
                if info is None or info['node kind'] != 'directory':
                    continue
            except CommandError:
                continue

            retval.append (module.strip ('/'))
                
        return retval

    def get_last_revision (self, uri):
        self._check_uri (uri)

        try:
            info = get_info (uri)
            if info is not None:
                return info['last changed rev']
        except:
            pass

        return None

register_backend ('svn', SVNRepository)
