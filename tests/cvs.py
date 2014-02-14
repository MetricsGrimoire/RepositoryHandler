#!/usr/bin/env python

import os
from repositoryhandler.backends import create_repository, \
    create_repository_from_path, RepositoryUnknownError
from repositoryhandler.backends.watchers import *
from tests import Test, register_test, remove_directory


def output(line, user_data):
    print "line(%s): %s" % (user_data, line),


class CVSTest(Test):

    def checkout(self):
        # checkout
        self.repo = create_repository(
            'cvs',
            ':pserver:anoncvs@anoncvs.freedesktop.org:/cvs/poppler')

        self.repo.add_watch(CHECKOUT, output, "check out")
        self.repo.checkout('poppler', '/tmp/')
        if not os.path.exists('/tmp/poppler/CVS'):
            print "CVS checkout: FAILED"
            return

        self.repo.checkout('poppler', '/tmp/', newdir='poppler-0.5',
                           rev='POPPLER_0_5_X')

        if os.path.exists('/tmp/poppler-0.5/CVS'):
            print "CVS checkout module: PASSED"
            try:
                repo2 = create_repository_from_path('/tmp/poppler-0.5/')
            except:
                print "CVS create_repository_from_path: FAILED"
                return
            try:
                repo2 = create_repository_from_path('/tmp/')
            except RepositoryUnknownError:
                print "CVS create_repository_from_path: PASSED"
            except:
                print "CVS create_repository_from_path: FAILED"
        else:
            print "CVS checkout: FAILED"

        # checkout of all modules module
        print "CVS checkout of all modules"
        self.repo.checkout('.', '/tmp/', newdir='poppler_modules-0.5',
                           rev='POPPLER_0_5_X')
        if not os.path.exists('/tmp/poppler_modules-0.5/CVS'):
            print "CVS checkout: FAILED"
            return
        print "CVS checkout: PASSED"

    def update(self):
        # update(other branch)
        self.repo.add_watch(UPDATE, output, "update")
        try:
            self.repo.update('/tmp/poppler', rev='POPPLER_0_5_X')
        except:
            print "CVS update: FAILED"
            return

        f = open('/tmp/poppler/CVS/Tag', 'r')
        tag = f.read(len('TPOPPLER_0_5_X'))
        f.close()
        if tag == 'TPOPPLER_0_5_X':
            print "CVS update: PASSED"
        else:
            print "CVS update: FAILED"

    def cat(self):
        def cat_output(line, user_data):
            user_data[0] += 1

        n_lines = [0]
        self.repo.add_watch(CAT, cat_output, n_lines)
        try:
            self.repo.cat('/tmp/poppler/goo/gmem.c', rev='1.2')
        except:
            print "CVS cat: FAILED"
            return

        if n_lines[0] == 204:
            print "CVS cat: PASSED"
        else:
            print "CVS cat: FAILED"

    def log(self):
        # log
        self.log_data = ""

        def log_cb(data, user_data=None):
            self.log_data += data

        self.repo.add_watch(LOG, log_cb)

        try:
            self.repo.log('/tmp/poppler', rev='POPPLER_0_5_X')
        except:
            print "CVS log: FAILED"
            return

        if len(self.log_data) > 0:
            print "CVS log: PASSED"
        else:
            print "CVS log: FAILED"
            return

        # Remote log
        try:
            self.log_data = ""
            self.repo.rlog('poppler', files=['ChangeLog'])
        except:
            print "CVS rlog: FAILED"
            return

        if len(self.log_data) > 0:
            print "CVS rlog: PASSED"
        else:
            print "CVS rlog: FAILED"

    def diff(self):
        try:
            self.repo.diff('/tmp/poppler', revs=['POPPLER_0_5_X'])
            self.repo.diff('/tmp/poppler', revs=['HEAD'])
            self.repo.diff('/tmp/poppler', revs=['1.1', '1.2'])
            self.repo.diff('/tmp/poppler', revs=['1.1', '1.2'],
                           files=['ChangeLog'])
            print "CVS diff: PASSED"
        except:
            print "CVS diff: FAILED"

    def blame(self):
        try:
            self.repo.blame('/tmp/poppler/ChangeLog', rev='1.2')
            self.repo.blame('/tmp/poppler/', files=['autogen.sh'])
            self.repo.blame('/tmp/poppler/', rev='1.1',
                            files=['README', 'README-XPDF'])
            print "CVS blame: PASSED"
        except:
            print "CVS blame: FAILED"

    def get_last_revision(self):
        try:
            rev = self.repo.get_last_revision('/tmp/poppler/ChangeLog')
            if rev is not None:
                print "CVS get_last_revision(%s): PASSED" % (rev)
                return
        except:
            pass

        print "CVS get_last_revision: FAILED"

    def clean(self):
        remove_directory('/tmp/poppler')
        remove_directory('/tmp/poppler-0.5')
        remove_directory('/tmp/poppler_modules-0.5')

register_test('cvs', CVSTest)
