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
from repositoryhandler.backends import Repository,\
    RepositoryInvalidWorkingCopy, register_backend, RepositoryCommandError
from repositoryhandler.backends.watchers import *


def get_config(path, option=None):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    cmd = ['git', 'config']

    if option is not None:
        cmd.extend(['--get', option])
    else:
        cmd.extend(['-l'])

    command = Command(cmd, path, env={'PAGER': ''})
    out = command.run_sync()

    if option is not None:
        return out.strip('\n\t ')

    retval = {}
    for line in out.splitlines():
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        retval[key.lower().strip()] = value.strip('\n\t ')

    if retval == {}:
        return None

    return retval


def get_repository_from_path(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)

    dir = path
    while dir and not os.path.isdir(os.path.join(dir, ".git")) and dir != "/":
        dir = os.path.dirname(dir)

    if not dir or dir == "/":
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a Git '
                                           'working copy' % path)
    try:
        uri = get_config(dir, 'remote.origin.url')
    except CommandError:
        uri = dir

    if uri is None or not uri:
        raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a Git '
                                           'working copy' % path)

    return 'git', uri


class GitRepository(Repository):
    '''Git Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'git')

        self.git_version = None

    def _check_uri(self, uri):
        type, repo_uri = get_repository_from_path(uri)
        if not repo_uri.startswith(self.uri):
            raise RepositoryInvalidWorkingCopy('"%s" does not appear to be a '
                                               'Git working copy (expected %s'
                                               ' but got %s)' %
                                               (uri, self.uri, repo_uri))

    def _get_git_version(self):
        if self.git_version is not None:
            return self.git_version

        cmd = ['git', '--version']

        command = Command(cmd)
        out = command.run_sync()
        # it could looks like:
        #  git version 1.7.10.4 // 1.8.4.rc3 // 1.7.12.4 (Apple Git-37) // 1.9.3 (Apple Git-50)

        version = out.replace("git version ", "")
        try:
            self.git_version = tuple([int(i) for i in version.split('.')])
        except ValueError:
            self.git_version = tuple([int(i) for i in version.split()[0].split('.')[0:3]])

        return self.git_version

    def _get_branches(self, path):
        cmd = ['git', 'branch']

        command = Command(cmd, path)
        out = command.run_sync()

        patt = re.compile("^\*(.*)$")

        i = 0
        current = 0
        retval = []
        for line in out.splitlines():
            if line.startswith(self.uri):
                continue

            match = patt.match(line)
            if match:
                current = i
                retval.append(match.group(1).strip(' '))
            else:
                retval.append(line.strip(' '))
            i += 1

        return current, retval

    def _checkout_branch(self, path, branch):
        self._check_uri(path)

        current, branches = self._get_branches(path)

        if branch in branches:
            if branches.index(branch) == current:
                return

            cmd = ['git', 'checkout', branch]
        else:
            cmd = ['git', 'checkout', '-b', branch, 'origin/%s' % (branch)]

        command = Command(cmd, path)
        command.run()

    def __get_root_dir(self, uri):
        if uri != self.uri:
            directory = os.path.dirname(uri)
            while directory and not os.path.isdir(os.path.join(directory,
                                                               ".git")):
                directory = os.path.dirname(directory)
        else:
            directory = uri

        return directory or self.uri

    def copy(self):
        repo = GitRepository(self.uri)
        repo.git_version = self.git_version
        return repo

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
            uri = os.path.join(self.uri, module)

        cmd = ['git', 'clone', uri]

        if newdir is not None:
            cmd.append(newdir)
        elif module == '.':
            cmd.append(os.path.basename(uri.rstrip('/')))
        else:
            cmd.append(module)

        def ignore_progress_stderr(*args):
            return True

        command = Command(cmd, rootdir,
                          error_handler_func=ignore_progress_stderr)
        self._run_command(command, CHECKOUT)

        if branch is not None:
            self._checkout_branch(srcdir, branch)

    def update(self, uri, rev=None):
        self._check_uri(uri)

        branch = rev
        if branch is not None:
            self._checkout_branch(uri, branch)

        cmd = ['git', 'pull']

        if os.path.isfile(uri):
            directory = os.path.dirname(uri)
        else:
            directory = uri

        command = Command(cmd, directory)
        self._run_command(command, UPDATE)

    def cat(self, uri, rev=None):
        self._check_uri(uri)

        cmd = ['git', 'show']

        cwd = self.__get_root_dir(uri)
        target = uri[len(cwd):].strip("/")

        if rev is not None:
            target = "%s:%s" % (rev, target)
        else:
            target = "HEAD:%s" % (target)

        cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, CAT)

    def size(self, uri, rev=None):
        self._check_uri(uri)

        cmd = ['git', 'cat-file', '-s']

        cwd = self.__get_root_dir(uri)
        target = uri[len(cwd):].strip("/")

        if rev is not None:
            target = "%s:%s" % (rev, target)
        else:
            target = "HEAD:%s" % (target)

        cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, SIZE)

    def log(self, uri, rev=None, files=None, gitref=None):
        self._check_uri(uri)

        if os.path.isfile(uri):
            cwd = os.path.dirname(uri)
            files = [os.path.basename(uri)]
        elif os.path.isdir(uri):
            cwd = uri
        else:
            cwd = os.getcwd()

        cmd = ['git', 'log', '--topo-order', '--pretty=fuller',
               '--parents', '--name-status', '-M', '-C', '-c']

        # Git < 1.6.4 -> --decorate
        # Git = 1.6.4 -> broken
        # Git > 1.6.4 -> --decorate=full
        try:
            major, minor, micro = self._get_git_version()
        except ValueError:
            major, minor, micro, extra = self._get_git_version()

        if major <= 1 and minor < 6:
            cmd.append('--decorate')
        elif major <= 1 and minor == 6 and micro <= 4:
            cmd.append('--decorate')
        else:
            cmd.append('--decorate=full')


        if gitref:
            cmd.append(gitref)
        else:
            try:
                get_config(uri, 'remote.origin.url')

                if major <= 1 and minor < 8:
                    cmd.append('origin')
                else:
                    cmd.append('--remotes=origin')
            except CommandError:
                pass
            cmd.append('--all')

        if rev is not None:
            cmd.append(rev)

        if files:
            cmd.append('--')
            for file in files:
                cmd.append(file)
        elif cwd != uri:
            cmd.append(uri)

        command = Command(cmd, cwd, env={'PAGER': ''})
        try:
            self._run_command(command, LOG)
        except RepositoryCommandError:
            pass

    def rlog(self, module=None, rev=None, files=None):
        # Not supported by Git
        return

    def diff(self, uri, branch=None, revs=None, files=None):
        self._check_uri(uri)

        if os.path.isfile(uri):
            cwd = self.__get_root_dir(uri)
            files = [uri[len(cwd):].strip("/")]
        elif os.path.isdir(uri):
            cwd = uri
        else:
            cwd = os.getcwd()

        cmd = ['git', 'diff']

        if revs is not None:
            if len(revs) == 1:
                cmd.append(revs[0])
            elif len(revs) > 1:
                cmd.append("%s..%s" % (revs[0], revs[1]))

        cmd.append("--")

        if files is not None:
            cmd.extend(files)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, DIFF)

    def show(self, uri, rev=None):
        self._check_uri(uri)

        if os.path.isfile(uri):
            cwd = self.__get_root_dir(uri)
            target = uri[len(cwd):].strip("/")
        elif os.path.isdir(uri):
            cwd = uri
            target = None
        else:
            cwd = os.getcwd()
            target = None

        cmd = ['git', 'show', '--pretty=format:']

        if rev is not None:
            cmd.append(rev)

        cmd.append("--")

        if target is not None:
            cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, DIFF)

    def blame(self, uri, rev=None, files=None, mc=False):
        self._check_uri(uri)

        if os.path.isfile(uri):
            cwd = os.path.dirname(uri)
            files = [os.path.basename(uri)]
        elif os.path.isdir(uri):
            cwd = uri
        else:
            cwd = os.getcwd()

        cmd = ['git', 'blame', '--root', '-l', '-t', '-f']

        if mc:
            cmd.extend(['-M', '-C'])

        if rev is not None:
            cmd.append(rev)
        else:
            try:
                get_config(uri, 'remote.origin.url')
                cmd.append('origin/master')
            except CommandError:
                pass

        cmd.append('--')

        # Git doesn't support multiple files
        # we take just the first one
        cmd.append(files and files[0] or uri)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, BLAME)

    def ls(self, uri, rev=None):
        self._check_uri(uri)

        target = None
        if os.path.isfile(uri):
            cwd = os.path.dirname(uri)
            target = os.path.basename(uri)
        elif os.path.isdir(uri):
            cwd = uri
        else:
            cwd = os.getcwd()

        if rev is None:
            try:
                get_config(uri, 'remote.origin.url')
                rev = 'origin/master'
            except CommandError:
                rev = 'HEAD'

        cmd = ['git',  'ls-tree', '--name-only', '--full-name', '-r', rev]

        if target is not None:
            cmd.append(target)

        command = Command(cmd, cwd, env={'PAGER': ''})
        self._run_command(command, LS)

    def get_modules(self):
        #Not supported by Git
        return []

    def get_last_revision(self, uri):
        self._check_uri(uri)

        cmd = ['git', 'rev-list', 'HEAD^..HEAD']

        command = Command(cmd, uri, env={'PAGER': ''})
        try:
            out = command.run_sync()
        except:
            return None

        if out == "":
            return None

        return out.strip('\n\t ')

    def is_ancestor(self, uri, rev1, rev2):
        self._check_uri(uri)
        version = self._get_git_version()

        if version[0] == 0 or (version[0] == 1 and version[1] < 8):
            # Should we implement an workaround for git under 1.8 or
            # just have git 1.8 or later in prerequisites?
            # An workaround can be found at
            # http://stackoverflow.com/a/3006203/1305362
            raise NotImplementedError

        # 'git merge-base --is-ancestor' is only supported after 1.8
        cmd = ['git', 'merge-base', '--is-ancestor', rev1, rev2]
        command = Command(cmd, uri, env={'PAGER': ''})
        try:
            command.run()
            return True
        except CommandError as e:
            if e.returncode == 1:
                return False
            else:
                raise e


register_backend('git', GitRepository)
