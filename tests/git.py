import os
import re
from repositoryhandler.backends import create_repository, create_repository_from_path, RepositoryUnknownError
from repositoryhandler.backends.watchers import *
from tests import Test, register_test, remove_directory

class GitTest (Test):

    def checkout (self):
        self.repo = create_repository ('git', 'git://git.kernel.org/pub/scm/')
        self.repo.checkout ('utils/kernel/cpufreq/cpufrequtils.git', '/tmp/', newdir = 'cpufrequtils')
        if not os.path.exists ('/tmp/cpufrequtils/.git'):
            print "Git checkout: FAILED"
            return

        self.repo.checkout ('utils/pciutils/pciutils.git', '/tmp/', newdir = 'pciutils', branch = 'network')
        if not os.path.exists ('/tmp/pciutils/.git'):
            print "Git checkout: FAILED"
            return
        
        try:
            repo2 = create_repository_from_path ('/tmp/cpufrequtils')
        except:
            print "Git create_repository_from_path: FAILED"
            return
        try:
            repo2 = create_repository_from_path ('/tmp/')
        except RepositoryUnknownError:
            print "Git create_repository_from_path: PASSED"
        except:
            print "Git create_repository_from_path: FAILED"
            return
            
        print "Git checkout: PASSED"

    def update (self):
        try:
            self.repo.update ('/tmp/cpufrequtils')
        except:
            print "Git update: FAILED"
            return

        try:
            self.repo.update ('/tmp/pciutils/', rev = 'master')
        except:
            print "Git update: FAILED"
            raise
        
        print "Git update: PASSED"

    def log (self):
        def log_cb (data, user_data = None):
            self.log_data += data

        self.repo.add_watch (LOG, log_cb)

        try:
            self.log_data = ""
            self.repo.log ('/tmp/pciutils/', files = ['ChangeLog'])
        except:
            print "Git log: FAILED"
            raise
            return

        if len (self.log_data) <= 0:
            print "Git log: FAILED"
            return

        print "Git log: PASSED"

    def diff (self):
        # TODO
        pass

    def get_modules (self):
        pass

    def get_last_revision (self):
        try:
            rev = self.repo.get_last_revision ('/tmp/cpufrequtils')
            if rev is not None:
                print "Git get_last_revision (%s): PASSED" % (rev)
                return
        except:
            pass

        print "Git get_last_revision: FAILED"

    def clean (self):
        remove_directory ('/tmp/cpufrequtils')
        remove_directory ('/tmp/pciutils')


register_test ('git', GitTest)
