# RepositoryHandler

## Description

RepositoryHandler is a python library for handling code repositories through a common interface.

## How to get RepositoryHandler

Latest version: ```git clone https://github.com/MetricsGrimoire/RepositoryHandler.git```

## Supported repository types

 * CVS
 * SVN
 * GIT
 * BZR (Preliminary support)
 * Tarball

Optional:

 * ARCH (not implemented yet)
 * DARCS (not implemented yet)

## Dependencies

 * Python >= 2.4
 * CVS client
 * SVN client
 * Git client
 * WGET or curl
 * Autoconf (for installation)

## How to install

To be used from other packages, RepositoryHandler should be installed:

     $ python setup.py install

If root access is not possible, the "sudo" command will not be run and the package will stay installed in the current directory. 

It can be used there by including it in the `PKG_CONFIG_PATH` environment variable.

## Examples

### CVS Repository

```python
from repositoryhandler.backends import create_repository

# create a cvs repository for poppler on FreeDesktop
repo = create_repository ('cvs', ':pserver:anoncvs@anoncvs.freedesktop.org:/cvs/poppler')

# checkout module poppler into /tmp directory from HEAD
repo.checkout ('poppler', '/tmp/')

# update working copy on /tmp from POPPLER_0_5_X branch
repo.update ('/tmp/poppler', rev = 'POPPLER_0_5_X')

# show diff between HEAD and POPPLER_0_5_X branches
diff = repo.diff ('/tmp/poppler', revs = ['HEAD', 'POPPLER_0_5_X'])
print diff

# show history for ChangeLog file
history = repo.log ('/tmp/poppler', files = ['ChangeLog'])
print history
```
