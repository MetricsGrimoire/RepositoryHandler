# tarball.py
#
# Copyright (C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
# Copyright (C) 2007 GSyC/LibreSoft Group
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

from repositoryhandler.Command import Command
from repositoryhandler.backends import Repository, register_backend
from repositoryhandler.backends.watchers import *
from repositoryhandler.Downloader import get_download_command

### FileExtractor
import tarfile
import zipfile
import gzip
import bz2


def is_gzipfile(uri):
    try:
        import gzip
        t = gzip.GzipFile(uri, "r")
        t.close()
        return True
    except:
        return False


def is_bz2file(uri):
    try:
        import bz2
        t = bz2.BZ2File(uri, "r")
        t.close()
        return True
    except:
        return False


class FileExtractorError(Exception):
    """
    Raised if an error occurs during the extraction process
    """

    def __init__(self, msg):
        Exception.__init__(self, msg)


class FileExtractor:

    def __init__(self, uri):
        self.uri = uri

    def extract(self, path=None):
        raise NotImplementedError


class TarFileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            tar = tarfile.open(self.uri, 'r:*')
        except tarfile.TarError, e:
            raise FileExtractorError("FileExtractor Error: Opening tarfile "
                                     "%s: %s" % (self.uri, str(e)))

        if path is None:
            path = os.cwd()

        try:
            tar.extractall(path)
        except tarfile.TarError, e:
            tar.close()
            raise FileExtractorError("FileExtractor Error: Extracting tarfile"
                                     " %s: %s" % (self.uri, str(e)))

        tar.close()


class ZipFileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            zip = zipfile.ZipFile(self.uri, 'r')
        except zipfile.BadZipfile, e:
            raise FileExtractorError("FileExtractor Error: Opening zipfile"
                                     " %s: %s" % (self.uri, str(e)))

        if path is None:
            path = os.cwd()

        for name in zip.namelist():
            try:
                fpath = os.path.join(path, name)

                # Check if 'name' is a directory
                if name[-1] == '/':
                    try:
                        os.makedirs(fpath)
                    except IOError, e:
                        zip.close()
                        raise FileExtractorError("FileExtractor Error: Write "
                                                 "error while extracting "
                                                 "zipfile %s: %s" %
                                                 (self.uri, str(e)))
                else:
                    bytes = zip.read(name)

                    f = open(fpath, 'w')
                    try:
                        f.write(bytes)
                    except IOError, e:
                        zip.close()
                        f.close()
                        raise FileExtractorError("FileExtractor Error: Write "
                                                 "error while extracting "
                                                 "zipfile %s: %s" %
                                                 (self.uri, str(e)))
                    f.close()
            except zipfile.BadZipfile, e:
                zip.close()
                raise FileExtractorError("FileExtractor Error: Reading "
                                         "zipfile %s: %s" % (self.uri, str(e)))
        zip.close()


class GzipFileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            gz = gzip.GzipFile(self.uri, 'r')
        except Exception, e:
            raise FileExtractorError("FileExtractor Error: Opening gzip "
                                     "%s: %s" % (self.uri, str(e)))

        if path is None:
            path = os.cwd()

        try:
            path = os.path.join(path,
                                self.uri.split("/")[-1].replace(".gz", ""))
            f = open(path, "w")
            f.write(gz.read())
            f.close()
        except Exception, e:
            gz.close()
            raise FileExtractorError("FileExtractor Error: Extracting gzip "
                                     "%s: %s" % (self.uri, str(e)))

        gz.close()


class Bzip2FileExtractor(FileExtractor):

    def __init__(self, uri):
        FileExtractor.__init__(self, uri)

    def extract(self, path=None):
        try:
            bz2 = bz2.BZ2File(self.uri, 'r')
        except Exception, e:
            raise FileExtractorError("FileExtractor Error: Opening bzip2 "
                                     "%s: %s" % (self.uri, str(e)))

        if path is None:
            path = os.cwd()

        try:
            path = os.path.join(path,
                                self.uri.split("/")[-1].replace(".bz2", ""))
            f = open(path, "w")
            f.write(bz2.read())
            f.close()
        except Exception, e:
            bz2.close()
            raise FileExtractorError("FileExtractor Error: Extracting bzip2"
                                     " %s: %s" % (self.uri, str(e)))

        bz2.close()


def create_file_extractor(uri):
    if tarfile.is_tarfile(uri):
        return TarFileExtractor(uri)
    elif zipfile.is_zipfile(uri):
        return ZipFileExtractor(uri)
    elif is_gzipfile(uri):
        return GzipFileExtractor(uri)
    elif is_b2file(uri):
        return Bzip2FileExtractor(uri)

    raise FileExtractorError("FileExtractor Error: URI '%s' doesn't look like "
                             "a valid tarball or compressed file" % (uri))


class TarballRepository(Repository):
    '''Tarball Repository'''

    def __init__(self, uri):
        Repository.__init__(self, uri, 'tarball')

    def copy(self):
        return TarballRepository(self.uri)

    def checkout(self, module, rootdir, newdir=None, branch=None, rev=None):
        if newdir is not None:
            srcdir = os.path.join(rootdir, newdir)
        else:
            srcdir = rootdir
        if not os.path.exists(srcdir):
            os.makedirs(srcdir)

        if os.path.exists(module):
            tarball_path = module
        else:
            # Download module to rootdir
            filename = os.path.basename(module).split('?')[0]
            tarball_path = os.path.join(srcdir, filename)
            cmd = get_download_command(module, tarball_path, '/dev/stdout')
            if cmd is None:
                return

            command = Command(cmd, srcdir)
            self._run_command(command, CHECKOUT)

            if not os.path.exists(tarball_path):
                return

        # Unpack the tarball
        fe = create_file_extractor(tarball_path)
        fe.extract(srcdir)

register_backend('tarball', TarballRepository)
