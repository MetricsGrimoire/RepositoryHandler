import sys
import os

__all__ = [
    'Test',
    'remove_directory',
    'register_test',
    'get_test'
]


class Test:

    def checkout(self):
        pass

    def update(self):
        pass

    def cat(self):
        pass

    def log(self):
        pass

    def rlog(self):
        pass

    def diff(self):
        pass

    def blame(self):
        pass

    def ls(self):
        pass

    def get_modules(self):
        pass

    def get_last_revision(self):
        pass

    def clean(self):
        pass

    def run(self):
        self.checkout()
        self.update()
        self.cat()
        self.log()
        self.diff()
        self.blame()
        self.ls()
        self.get_modules()
        self.get_last_revision()
        self.clean()


def remove_directory(path):
    if not os.path.exists(path):
        return

    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))

    os.rmdir(path)


_tests = {}


def register_test(test_name, test_class):
    _tests[test_name] = test_class


def get_test(test_name):
    if test_name not in _tests:
        try:
            __import__(test_name)
        except:
            pass

    if test_name not in _tests:
        sys.stderr.write('Test %s not found\n' % (test_name))
        return None

    return _tests[test_name]
