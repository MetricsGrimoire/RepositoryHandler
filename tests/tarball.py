#!/usr/bin/env python

import os
from repositoryhandler.backends import create_repository
from tests import Test, register_test, remove_directory


class TarballTest (Test):

    def checkout(self):
        # checkout
        self.repo = create_repository('tarball', None)
        self.repo.checkout(
            'http://cairographics.org/snapshots/pycairo-0.4.0.tar.gz', '/tmp/')
        if not os.path.exists('/tmp/pycairo-0.4.0.tar.gz'):
            print "Tarball checkout: FAILED"
            return
        elif not os.path.exists('/tmp/pycairo-0.4.0/ChangeLog'):
            print "Tarball checkout: FAILED"
            return

        # checkout with local path
        self.repo.checkout('/tmp/pycairo-0.4.0.tar.gz', '/tmp/pycairo-local')
        if not os.path.exists('/tmp/pycairo-local/pycairo-0.4.0/ChangeLog'):
            print "Tarball checkout: FAILED"
            return

        # Mbox
        self.repo.checkout('http://lists.morfeo-project.org/pipermail/'
                           'libresoft-tools-devel/2007-April.txt.gz',
                           '/tmp')
        if not os.path.exists('/tmp/2007-April.txt'):
            print "Tarball checkout: FAILED"
            return

        print "Tarball checkout: PASSED"

        # TODO: check zip

    def clean(self):
        os.remove('/tmp/pycairo-0.4.0.tar.gz')
        remove_directory('/tmp/pycairo-0.4.0/')
        remove_directory('/tmp/pycairo-local')
        os.remove('/tmp/2007-April.txt')

register_test('tarball', TarballTest)
