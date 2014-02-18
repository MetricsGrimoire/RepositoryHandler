## Repository Handler 0.5

### New features and API changes

* Support for authentication in Subversion repositories (The authentication is supported by passing user and password within the URL (i.e https://user:passwd@svn.example.org)).
* PEP8

### Bug fixes

* SSL certificates in Subversion backend
* Streams not ended by '\n' are fully read
* Typos

### Thanks to all contributors

* Luis Cañas Díaz
* Jesús M. Gonzalez-Barahona
* Santiago Dueñas
* Alvaro del Castillo
* Alexander Pepper

## Repository Handler 0.4

### New features and API changes

* Add `cat()` method to the API to be able to output the content of any uri for any given revision. Implement the `cat()` method in CVS, SVN and git backends adding tests for all of them too.
* Make `get_repository_from_path()` work even for deleted paths.
* Make `cat()` in CVS backend work even for deleted paths.
* Adds `-N` parameter to CVS checkout command
* Add `ls` command to list repository files
* Use remote/origin as default revision in Git
* Use `-f` option in blame command for Git. Show filename in the original commit. By default filename is shown if there is any line that came from a file with different name, due to rename detection.
* Add `mc` parameter to blame method to detect moves and renames
* Make `get_uri_for_path()` work for non-dir paths
* Add `--` to blame command line in Git backend. It makes git find paths in older revisions that have been renamed, moved or deleted.
* Implement `diff` in Git backend
* Add `get_root_dir()` private function in Git backend
* Add a new method `show()` to get the patch of a given revision
* Implement `show()` both for SVN and Git backends

### Bug fixes

* Handle runtime errors of CVS and SVN commands. Fixes bug #31. Command has been changed to allow handling errors during command execution, instead of always raising `CommandRunningError`.
* Fix blame method to match parent signature both for CVS and SVN backends.
* Fix blame method to match parent signature for SVN backend
* Fix blame when url contains an `@` for SVN. If the url or filename contains an `@` svn fails with a syntax error because `@` is the revision separator.
* Avoid the crash in Git when path points to a file in `get_config()` and `get_repository_from_path()`
* Fix log command depending on git version. Since version 1.6.5 `--decorate` command line option accepts two parameters: `short` and `full`. We need to use the full version which was the default one before git 1.6.4
* Fix variable name conflict for Git backend. Spotted by Philip Makedonski.
* Fix variable name in `cat()` for Git backend. Fixes bug #244.
* Fix infinite loop when uri is invalid or doesn't contain / for Git backend.

### Documentation

* Added how to get it
* Installation instructions

### Thanks to all contributors

* Carlos García Campos
* Jesús M. Gonzalez-Barahon
* Santiago Dueñas
* Philip Makedonski
* Juan F. Gato Luis

## Repository Handler 0.3

### New features and API changes

* Add pkg-config file. (Carlos Garcia Campos)
* A new method has been added to be able to get the repository URI corresponding to a local path where the repository was checked out. (Carlos Garcia Campos)

### Bug fixes

* Do not use git- commands, they are not available in recent git versions. (Carlos Garcia Campos)
* Implement the special case `module = '.'` in the git backend to be able to clone the whole repository. (Carlos Garcia Campos)
* Improve error handling when running commands providing the exceptions `RepositoryCommandError` and `RepositoryCommandRunningError` that wrap the `Command.py` exceptions. (Carlos Garcia Campos)
* Several fixes and improvements when running commands included in the `Command.py` module. One important improvement is that standard and error output are not stored in memory anymore when the `run()` function is called with callbacks to handle such output, since it caused memory problems with commands that produces a lot of output like the log command. (Carlos Garcia Campos)
      
## Repository Handler 0.2

### New features and API changes

* Add `blame` support. (Miguel Angel Tinte, Carlos Garcia Campos)
* The `git log` output is even more detailed now including information about tags and branchces (Carlos Garcia Campos)
* Add `rlog` method (only implemented by CVS and SVN backends) to get the log directly from the repository. (Carlos Garcia Campos)
* Implement `get_last_revision` method in CVS backend (Carlos Garcia Campos)
* Add a debug option to be able to know what commands are being executed (Carlos Garcia Campos)
* Include tags information in CVS log output (Carlos Garcia Campos)
* Branch parameter has been removed from log method (Carlos Garcia Campos)
* Add an option to force update in SVN backend (Santiago Dueñas)
* Initial Bazaar support (Carlos Garcia Campos)

### Bug fixes

* Fix ssl certificate handling in SVN backend (Carlos Garcia Campos)
* Fix checkout of deleted files in SVN backend (Luis Cañas)
* Several fixes in commands execution and communication. (Carlos Garcia Campos)

## Repository Handler 0.1

* First public release
