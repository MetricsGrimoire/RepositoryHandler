import os
import re
from repositoryhandler.backends import create_repository,\
    create_repository_from_path, RepositoryUnknownError
from repositoryhandler.backends.watchers import *
from tests import Test, register_test, remove_directory


class BzrTest(Test):

    def checkout(self):
        self.repo = create_repository('bzr',
                                      'http://pkg-config.freedesktop.org/bzr/')
        self.repo.checkout('pkg-config', '/tmp/', newdir='pkg-config')
        if not os.path.exists('/tmp/pkg-config/.bzr'):
            print "Bzr checkout: FAILED"
            return

        try:
            repo2 = create_repository_from_path('/tmp/pkg-config')
        except:
            print "Bzr create_repository_from_path: FAILED"
            return

        print "Bzr checkout: PASSED"

    def update(self):
        try:
            self.repo.update('/tmp/pkg-config')
        except:
            print "Bzr update: FAILED"
            return

        # TODO
        #try:
        #    self.repo.update('/tmp/pciutils/', rev = 'master')
        #except:
        #    print "Git update: FAILED"
        #    raise
        print "Bzr update: PASSED"

    def log(self):
        def log_cb(data, user_data=None):
            self.log_data += data

        self.repo.add_watch(LOG, log_cb)

        try:
            self.log_data = ""
            self.repo.log('/tmp/pkg-config/')
        except:
            print "Bzr log: FAILED"
            raise
            return

        if len(self.log_data) <= 0:
            print "Bzr log: FAILED"
            return

        print "Bzr log: PASSED"

    def diff(self):
        # TODO
        pass

    def get_modules(self):
        pass

    def get_last_revision(self):
        try:
            rev = self.repo.get_last_revision('/tmp/pkg-config')
            if rev is not None:
                print "Bzr get_last_revision(%s): PASSED" % (rev)
                return
        except:
            pass

        print "Bzr get_last_revision: FAILED"

    def clean(self):
        remove_directory('/tmp/pkg-config')

register_test('bzr', BzrTest)
