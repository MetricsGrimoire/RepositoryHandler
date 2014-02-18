#!/usr/bin/env python

import os
import re
from repositoryhandler.backends import create_repository,\
    create_repository_from_path, RepositoryUnknownError
from repositoryhandler.backends.watchers import *
from tests import Test, register_test, remove_directory


class SVNTest(Test):

    def checkout(self):
        # checkout
        self.repo = create_repository('svn',
                                      'http://svn.gnome.org/svn/gnome-common')
        self.repo.checkout('gnome-common', '/tmp/', branch="trunk", rev="3910")
        if not os.path.exists('/tmp/gnome-common/.svn') or \
                self.repo.get_last_revision('/tmp/gnome-common') != "3910":
            print "SVN checkout: FAILED"
            return

        self.repo.checkout('gnome-common', '/tmp/', newdir='gnome-common-2.16',
                           branch='gnome-2-16')
        if os.path.exists('/tmp/gnome-common-2.16/.svn'):
            print "SVN checkout: PASSED"
            try:
                repo2 = create_repository_from_path('/tmp/gnome-common-2.16')
            except:
                print "SVN create_repository_from_path: FAILED"
                return
            try:
                repo2 = create_repository_from_path('/tmp/')
            except RepositoryUnknownError:
                print "SVN create_repository_from_path: PASSED"
            except:
                print "SVN create_repository_from_path: FAILED"
        else:
            print "SVN checkout: FAILED"
            return

        try:
            # Repository without trunk dir
            repo2 = create_repository(
                'svn',
                'https://svn.forge.morfeo-project.org/svn/libresoft-tools')

            repo2.checkout('octopus/trunk', '/tmp/', newdir='octopus')
            if not os.path.exists('/tmp/octopus/.svn'):
                print "SVN checkout repo without /trunk: FAILED"
                return
        except:
            print "SVN checkout repo without /trunk: FAILED"
            return

        print "SVN checkout repo without /trunk: PASSED"

        try:
            # Download unconditionally the whole repo
            repo3 = create_repository('svn',
                                      'http://svn.gnome.org/svn/asyncworker')
            repo3.checkout('.', '/tmp/')
            if not os.path.exists('/tmp/asyncworker/.svn'):
                print "SVN checkout the whole repo: FAILED"
                return
        except:
            print "SVN checkout the whole repo: FAILED"
            return

        print "SVN checkout the whole repo: PASSED"

    def update(self):
        # update(other branch)
        try:
            self.repo.update('/tmp/gnome-common', rev='3900')
        except:
            print "SVN update: FAILED"
            return

        print "SVN update: PASSED"

    def cat(self):
        def cat_output(line, user_data):
            user_data[0] += 1

        n_lines = [0]
        self.repo.add_watch(CAT, cat_output, n_lines)
        # cat a file using a local path
        try:
            self.repo.cat('/tmp/gnome-common/ChangeLog')
        except:
            print "SVN cat: FAILED"
            return

        if n_lines[0] != 795:
            print "SVN cat: FAILED"
            return

        n_lines[0] = 0

        # cat a file using a remote path
        try:
            self.repo.cat(
                "http://svn.gnome.org/svn/gnome-common/trunk/ChangeLog",
                rev="3900")
        except:
            print "SVN cat: FAILED"
            return

        if n_lines[0] != 795:
            print "SVN cat: FAILED"
        else:
            print "SVN cat: PASSED"

    def log(self):
        # log(current branch)

        def log_cb(data, user_data=None):
            self.log_data += data

        self.repo.add_watch(LOG, log_cb)

        try:
            # Using a local path
            self.log_data = ""
            self.repo.log('/tmp/gnome-common', files=['ChangeLog'])
        except:
            print "SVN log: FAILED"
            return

        if len(self.log_data) <= 0:
            print "SVN log: FAILED"
            return

        try:
            # Using an URI
            self.log_data = ""
            self.repo.log('http://svn.gnome.org/svn/gnome-common/trunk',
                          files=['ChangeLog'])
        except:
            print "SVN log: FAILED"
            return

        if len(self.log_data) <= 0:
            print "SVN log: FAILED"

        # Repository without trunk dir
        repo2 = create_repository(
            'svn',
            'https://svn.forge.morfeo-project.org/svn/libresoft-tools')
        repo2.add_watch(LOG, log_cb)
        try:
            self.log_data = ""
            repo2.rlog('octopus/trunk')
        except:
            print "SVN rlog: FAILED"
            return

        if len(self.log_data) <= 0:
            print "SVN rlog: FAILED"
        else:
            print "SVN rlog: PASSED"

    def diff(self):
        try:
            # Using a local path
            self.repo.diff('/tmp/gnome-common', files=['ChangeLog'],
                           revs=['3900', '3901'])
        except:
            print "SVN diff: FAILED"
            return

        try:
            # Using an URI
            self.repo.diff('http://svn.gnome.org/svn/gnome-common',
                           branch='gnome-2-16',
                           files=['macros/autogen.sh'],
                           revs=['3875', '2834'])
            print "SVN diff: PASSED"
        except:
            print "SVN diff: FAILED"

    def blame(self):
        try:
            # Local path with single file
            self.repo.blame('/tmp/gnome-common/ChangeLog', rev='3900')
        except:
            print "SVN blame: FAILED"
            return

        try:
            # Local path several files
            self.repo.blame('/tmp/gnome-common/',
                            files=['autogen.sh', 'ChangeLog'])
        except:
            print "SVN blame: FAILED"
            return

        try:
            # Remote uri
            self.repo.blame(
                'http://svn.gnome.org/svn/gnome-common/trunk/ChangeLog',
                rev='3901')
        except:
            print "SVN blame: FAILED"
            return

        print "SVN blame: PASSED"

    def get_modules(self):
        try:
            # First layout
            repo = create_repository('svn',
                                     'http://svn.gnome.org/svn/gnome-common')
            module = repo.get_modules()
            if module[0] != 'gnome-common':
                print "SVN get_modules: FAILED"
                return
        except:
            print "SVN get_modules: FAILED"
            return

        try:
            # Second layout
            repo = create_repository(
                'svn',
                'https://svn.forge.morfeo-project.org/svn/libresoft-tools')
            modules = repo.get_modules()
            if len(modules) <= 0:
                print "SVN get_modules: FAILED"
                return
        except:
            print "SVN get_modules: FAILED"
            return

        print "SVN get_modules: PASSED"

    def get_last_revision(self):
        try:
            rev = self.repo.get_last_revision('/tmp/gnome-common')
            if rev is not None:
                print "SVN get_last_revision(%s): PASSED" % (rev)
                return
        except:
            pass

        print "SVN get_last_revision: FAILED"

    def clean(self):
        remove_directory('/tmp/gnome-common')
        remove_directory('/tmp/gnome-common-2.16')
        remove_directory('/tmp/octopus/')
        remove_directory('/tmp/atunes')

register_test('svn', SVNTest)
