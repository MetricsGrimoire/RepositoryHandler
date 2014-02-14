import os
import re
from repositoryhandler.backends import create_repository, \
    create_repository_from_path, RepositoryUnknownError
from repositoryhandler.backends.watchers import *
from tests import Test, register_test, remove_directory


class GitTest(Test):

    def checkout(self):
        self.repo = create_repository('git', 'git://git.kernel.org/pub/scm/')
        self.repo.checkout('utils/kernel/cpufreq/cpufrequtils.git', '/tmp/',
                           newdir='cpufrequtils')
        if not os.path.exists('/tmp/cpufrequtils/.git'):
            print "Git checkout: FAILED"
            return

        self.repo.checkout('utils/pciutils/pciutils.git', '/tmp/',
                           newdir='pciutils', branch='network')
        if not os.path.exists('/tmp/pciutils/.git'):
            print "Git checkout: FAILED"
            return

        # Test module='.'
        repo2 = create_repository('git',
                                  'git://anongit.freedesktop.org/libspectre')
        repo2.checkout('.', '/tmp')
        if not os.path.exists('/tmp/libspectre/.git'):
            print "Git checkout(module='.'): FAILED"
            return

        try:
            repo2 = create_repository_from_path('/tmp/cpufrequtils')
        except:
            print "Git create_repository_from_path: FAILED"
            return
        try:
            repo2 = create_repository_from_path('/tmp/')
        except RepositoryUnknownError:
            print "Git create_repository_from_path: PASSED"
        except:
            print "Git create_repository_from_path: FAILED"
            return

        print "Git checkout: PASSED"

    def update(self):
        try:
            self.repo.update('/tmp/cpufrequtils')
        except:
            print "Git update: FAILED"
            return

        try:
            self.repo.update('/tmp/pciutils/', rev='master')
        except:
            print "Git update: FAILED"
            return

        print "Git update: PASSED"

    def cat(self):
        def cat_output(line, user_data):
            user_data[0] += 1

        n_lines = [0]
        self.repo.add_watch(CAT, cat_output, n_lines)
        try:
            self.repo.cat("/tmp/cpufrequtils/lib/cpufreq.c",
                          rev="e982c5fc03f594d4c0384c4a35d761f64acb9273")
        except:
            print "Git cat: FAILED"
            return

        if n_lines[0] == 234:
            print "Git cat: PASSED"
        else:
            print "Git cat: FAILED"

    def log(self):
        def log_cb(data, user_data=None):
            self.log_data += data

        self.repo.add_watch(LOG, log_cb)

        try:
            self.log_data = ""
            self.repo.log('/tmp/pciutils/', files=['ChangeLog'])
        except:
            print "Git log: FAILED"
            return

        if len(self.log_data) <= 0:
            print "Git log: FAILED"
            return

        print "Git log: PASSED"

    def diff(self):
        # TODO
        pass

    def blame(self):
        def log_cb(data, user_data=None):
            self.blame_data += data

        self.repo.add_watch(BLAME, log_cb)

        try:
            self.blame_data = ""
            self.repo.blame('/tmp/pciutils/', files=['ChangeLog'])
        except:
            print "Git blame: FAILED"
            return

        if len(self.blame_data) <= 0:
            print "Git blame: FAILED"
            return

        print "Git blame: PASSED"

    def get_modules(self):
        pass

    def get_last_revision(self):
        try:
            rev = self.repo.get_last_revision('/tmp/cpufrequtils')
            if rev is not None:
                print "Git get_last_revision(%s): PASSED" % (rev)
                return
        except:
            pass

        print "Git get_last_revision: FAILED"

    def clean(self):
        remove_directory('/tmp/cpufrequtils')
        remove_directory('/tmp/pciutils')
        remove_directory('/tmp/libspectre')


register_test('git', GitTest)
