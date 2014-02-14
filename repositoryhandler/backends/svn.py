# svn.py
#
# Copyright(C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.
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

from repositoryhandler.Command import Command, CommandError,\
    CommandRunningError
from repositoryhandler.backends import(Repository,
                                       RepositoryInvalidWorkingCopy,
                                       RepositoryInvalidBranch,
                                       register_backend)
from repositoryhandler.backends.watchers import *

SSL_CERTIFICATE_QUESTION = "(R)eject, accept (t)emporarily "\
                           "or accept (p)ermanently?"


def run_command_sync(command):
    def error_handler(cmd, error):
        # Read error message
        question = error.split('\n')[-1]
        if question.strip() == SSL_CERTIFICATE_QUESTION:
            cmd.input('p\n')
            return True

        return False

    command.set_error_handler(error_handler)
    return command.run()


def get_auth_info(uri):
    import re

    auth = {'uri': uri,
            'user': None,
            'password': None}

    m = re.compile("^.*://(.+):(.+)@.*$").match(uri)
    if m is not None:
        auth['user'] = m.group(1)
        auth['password'] = m.group(2)
        auth['uri'] = uri.replace(auth['user'] + ':'
                                  + auth['password'] + '@', '')
    return auth


def get_info(uri, user=None, passwd=None):
    if os.path.isdir(uri):
        path = uri
        uri = '.'
    else:
        path = '.'

    if (user is not None) and (passwd is not None):
        cmd = ['svn', 'info', uri, '--username', user, '--password', passwd]
    else:
        cmd = ['svn', 'info', uri]

    command = Command(cmd, path, env={'LC_ALL': 'C'})
    out = run_command_sync(command)

    retval = {}
    for line in out.splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        retval[key.lower().strip()] = value.strip()

    if retval == {} or (uri in retval and retval[uri] == '(Not a valid URL)'):
        return None

    return retval


def list_files(uri, user=None, passwd=None):
    if os.path.isdir(uri):
        path = uri
        uri = '.'
    else:
        path = '.'

    if (user is not None) and (passwd is not None):
        cmd = ['svn', 'ls', uri, '--username', user, '--password', passwd]
    else:
        cmd = ['svn', 'ls', uri]

    command = Command(cmd, path, env={'LC_ALL': 'C'})
    out = run_command_sync(command)

    retval = []
    for line in out.splitlines():
        retval.append(line.strip())

    return retval


def get_repository_from_path(path):
    # Just in case path is a file
    if os.path.isfile(path):
        path = os.path.dirname(path)

    try:
        info = get_info(path)
    except CommandError:
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a SVN '
                                           'working copy' % path)

    if info is None:
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a SVN '
                                           'working copy' % path)

    return 'svn', info['repository root']


class SVNRepository(Repository):
    '''SVN Repository'''

    def __init__(self, uri, user=None, passwd=None):
        try:
            auth = get_auth_info(uri)

            if (user is not None) and (passwd is not None):
                self.user = user
                self.passwd = passwd
            else:
                self.user = auth['user']
                self.passwd = auth['password']

            info = get_info(auth['uri'], self.user, self.passwd)
            root = info['repository root']
        except:
            root = uri

        Repository.__init__(self, root, 'svn')

    def get_uri_for_path(self, path):
        self._check_uri(path)

        try:
            info = get_info(path)
        except:
            return self.uri

        return info['url']

    def _run_command(self, command, type, input=None):
        try:
            Repository._run_command(self, command, type, input)
        except CommandRunningError, e:
            # Read error message
            question = e.error.split('\n')[-1]
            if question.strip() == SSL_CERTIFICATE_QUESTION:
                Repository._run_command(self, command, type, 'p\n')

    def _get_command_auth(self, command):
        if (self.user is not None) and (self.passwd is not None):
            return command + ['--username', self.user,
                              '--password', self.passwd]
        return command

    def _check_uri(self, uri):
        def is_local(uri):
            import re
            return re.compile("^.*://.*$").match(uri) is None

        if is_local(uri):
            type, repo_uri = get_repository_from_path(uri)
            if repo_uri != self.uri:
                raise RepositoryInvalidWorkingCopy('"%s" does not appear to be'
                                                   ' a SVN working copy '
                                                   '(expected %s but got %s)'
                                                   % (uri, self.uri, repo_uri))
        else:
            if not uri.startswith(self.uri):
                raise RepositoryInvalidWorkingCopy('"%s" does not appear to be'
                                                   ' a SVN working copy for '
                                                   'repository %s'
                                                   % (uri, self.uri))

    def __get_uri_for_branch(self, module, branch):
        if branch is None:
            uri = os.path.join(self.uri, module)
        elif branch == 'trunk':
            uri = os.path.join(self.uri, 'trunk')
        else:
            uri = os.path.join(self.uri, 'branches', branch)

        try:
            info = get_info(uri)
            if info is not None:
                return uri
        except CommandError:
            raise RepositoryInvalidBranch('Invalid branch name "%s" for '
                                          'repository %s' % (branch, self.uri))

        return uri

    def copy(self):
        return SVNRepository(self.uri, self.user, self.passwd)

    def checkout(self, module, rootdir, newdir=None, branch=None, rev=None):
        if newdir is not None:
            srcdir = os.path.join(rootdir, newdir)
        elif newdir == '.':
            srcdir = rootdir
        else:
            if module == '.':
                srcdir = os.path.join(rootdir,
                                      os.path.basename(self.uri.rstrip('/')))
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

        # module == '.' is a special case to download the whole repository
        if module == '.':
            uri = self.uri
        else:
            uri = self.__get_uri_for_branch(module, branch)

        if rev is not None:
            uri += "@%s" % (rev)

        cmd = ['svn', 'checkout', uri]
        cmd = self._get_command_auth(cmd)

        if newdir is not None:
            cmd.append(newdir)
        elif module == '.':
            cmd.append(os.path.basename(uri.rstrip('/')))
        else:
            cmd.append(module)

        command = Command(cmd, rootdir, env={'LC_ALL': 'C'})
        self._run_command(command, CHECKOUT)

    def update(self, uri, rev=None, force=False):
        repo_uri = get_auth_info(uri)['uri']

        if not force:
            self._check_uri(repo_uri)

        cmd = ['svn', 'update']
        cmd = self._get_command_auth(cmd)

        if rev is not None:
            cmd.extend(['-r', rev])

        cmd.append(repo_uri)
        command = Command(cmd, env={'LC_ALL': 'C'})
        self._run_command(command, UPDATE)

    def cat(self, uri, rev=None):
        repo_uri = get_auth_info(uri)['uri']

        self._check_uri(repo_uri)

        if os.path.exists(repo_uri):
            cwd = os.path.dirname(repo_uri)
            target = os.path.basename(repo_uri)
        else:
            cwd = os.getcwd()
            target = repo_uri

        cmd = ['svn', 'cat']
        cmd = self._get_command_auth(cmd)

        if rev is not None:
            target += '@%s' % (rev)

        cmd.append(target)

        command = Command(cmd, cwd, env={'LC_ALL': 'C'})
        self._run_command(command, CAT)

    def log(self, uri, rev=None, files=None):
        repo_uri = get_auth_info(uri)['uri']

        self._check_uri(repo_uri)

        if os.path.isfile(repo_uri):
            cwd = os.path.dirname(repo_uri)
            target = '.'
        elif os.path.isdir(repo_uri):
            cwd = repo_uri
            target = '.'
        else:
            cwd = os.getcwd()
            target = repo_uri

        cmd = ['svn', '-v', 'log']
        cmd = self._get_command_auth(cmd)

        if rev is not None:
            cmd.extend(['-r', rev])

        if files is not None:
            if target != '.':
                cmd.append(target)
            for file in files:
                cmd.append(file)
        else:
            cmd.append(target)

        command = Command(cmd, cwd, env={'LC_ALL': 'C'})
        self._run_command(command, LOG)

    def rlog(self, module=None, rev=None, files=None):
        if module is not None:
            uri = os.path.join(self.uri, module.strip("/"))
        else:
            uri = self.uri

        self.log(uri, rev, files)

    def diff(self, uri, branch=None, revs=None, files=None):
        repo_uri = get_auth_info(uri)['uri']

        self._check_uri(repo_uri)

        if os.path.isfile(repo_uri):
            cwd = os.path.dirname(repo_uri)
            target = '.'
        elif os.path.isdir(repo_uri):
            cwd = repo_uri
            target = '.'
        else:
            target = repo_uri
            cwd = os.getcwd()

        cmd = ['svn', 'diff']
        cmd = self._get_command_auth(cmd)

        if revs is not None:
            if len(revs) == 1:
                cmd.extend(['-r', revs[0]])
            elif len(revs) > 1:
                cmd.extend(['-r', revs[0] + ':' + revs[1]])

        if files is not None:
            for file in files:
                if target == '.':
                    cmd.append(file)
                else:
                    cmd.append(os.path.join(target, file))
        else:
            cmd.append(target)

        command = Command(cmd, cwd, env={'LC_ALL': 'C'})
        self._run_command(command, DIFF)

    def show(self, uri, rev=None):
        repo_uri = get_auth_info(uri)['uri']

        self._check_uri(repo_uri)

        if os.path.isfile(repo_uri):
            cwd = os.path.dirname(repo_uri)
            target = os.path.basename(repo_uri)
        elif os.path.isdir(repo_uri):
            cwd = repo_uri
            target = '.'
        else:
            target = repo_uri
            cwd = os.getcwd()

        if rev is None:
            info = get_info(repo_uri, self.user, self.passwd)
            rev = info['last changed rev']

        cmd = ['svn', 'diff', '-c', rev, target]
        cmd = self._get_command_auth(cmd)

        command = Command(cmd, cwd, env={'LC_ALL': 'C'})
        self._run_command(command, DIFF)

    def blame(self, uri, rev=None, files=None, mc=False):
        repo_uri = get_auth_info(uri)['uri']

        # In SVN the path already contains the branch info
        # so no need for a branch parameter
        self._check_uri(repo_uri)

        if os.path.isfile(repo_uri):
            cwd = os.path.dirname(repo_uri)
            target = os.path.basename(repo_uri)
        elif os.path.isdir(repo_uri):
            cwd = repo_uri
            target = '.'
        else:
            cwd = os.getcwd()
            target = repo_uri

        if rev is not None and target != '.':
            target += "@%s" % (rev)
        else:
            # If the target contains an '@' we need to add
            # another '@' at the end so that the first one is
            # not considered as revision separator by svn
            if '@' in target:
                target += '@'

        cmd = ['svn', '-v', 'blame']
        cmd = self._get_command_auth(cmd)

        if files is not None:
            if target != '.':
                cmd.append(target)

            for file in files:
                if rev is not None:
                    file += "@%s" % (rev)
                cmd.append(file)
        else:
            cmd.append(target)

        command = Command(cmd, cwd, env={'LC_ALL': 'C'})
        self._run_command(command, BLAME)

    def ls(self, uri, rev=None):
        repo_uri = get_auth_info(uri)['uri']

        self._check_uri(repo_uri)

        if os.path.isfile(repo_uri):
            cwd = os.path.dirname(repo_uri)
            target = os.path.basename(repo_uri)
        elif os.path.isdir(repo_uri):
            cwd = repo_uri
            target = '.'
        else:
            cwd = os.getcwd()
            target = repo_uri

        cmd = ['svn', '-R', 'ls']
        cmd = self._get_command_auth(cmd)

        if rev is not None:
            if target == '.':
                cmd.extend(['-r', rev])
            else:
                target += "@%s" % (rev)

        cmd.append(target)

        command = Command(cmd, cwd, env={'LC_ALL': 'C'})
        self._run_command(command, LS)

    def get_modules(self):
        # Two 'standard' repository layouts
        # repo/trunk repo/branches
        #
        # repo/project1/trunk repo/project1/branches
        # repo/project2/trunk repo/project2/branches
        #
        # See Version Control with Subversion, page 98
        #

        # Try the first layout
        uri = os.path.join(self.uri, 'trunk')
        try:
            info = get_info(uri, self.user, self.passwd)
            if info is not None:
                return [self.uri.split('/')[-1]]
        except CommandError:
            # Try with the other layout
            pass

        # Second layout
        retval = []
        modules = list_files(self.uri)
        for module in modules:
            uri = os.path.join(self.uri, module, 'trunk')

            try:
                info = get_info(uri, self.user, self.passwd)
                if info is None or info['node kind'] != 'directory':
                    continue
            except CommandError:
                continue

            retval.append(module.strip('/'))

        return retval

    def get_last_revision(self, uri):
        repo_uri = get_auth_info(uri)['uri']

        self._check_uri(repo_uri)
        try:
            info = get_info(repo_uri, self.user, self.passwd)
            if info is not None:
                return info['last changed rev']
        except:
            pass

        return None

register_backend('svn', SVNRepository)
