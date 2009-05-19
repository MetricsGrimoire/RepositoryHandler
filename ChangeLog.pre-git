2009-04-30  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/cvs.py:
	* tests/cvs.py:

	Make cat() in CVS backend work even for deleted paths.
	
2009-04-28  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/git.py:

	Make get_repository_from_path() work even for deleted paths.
	
2009-03-31  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/watchers.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	* tests/__init__.py:
	* tests/cvs.py:
	* tests/git.py:
	* tests/svn.py:

	Add cat method to the API to be able to output the content of any
	uri for any given revision. Implement the cat method in cvs, svn
	and git backends adding tests for all of them too.
	
2009-03-29  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* configure.in:
	* NEWS:

	Update for release 0.3
	
2009-03-11  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/Command.py:
	* repositoryhandler/backends/cvs.py:

	Update Command from misc and move code specific of the cvs diff
	exception from Command to the CVS backend.
	
2009-03-11  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* configure.in:
	* Makefile.am:
	* repositoryhandler.pc.in:

	Add pkg-config file.
	
2009-03-11  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/__init__.py:

	Add exceptions to __all__ list.
	
2009-03-11  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/__init__.py:

	Add RepositoryCommandError and RepositoryCommandRunningError
	exceptions to wrap Command exceptions.
	
2009-03-10  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/git.py:

	Do not use git- commands since it's deprecated and even not
	available in recent git versions.
	
2009-03-10  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/git.py:
	* tests/git.py:

	Implement the special case module = '.' in the git backend to be
	able to clone the whole repository.
	
2009-03-10  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/svn.py:

	Run svn checkout and update with the C locale too for the error
	messages.
	
2009-03-04  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/Command.py:

	Updated from misc. Several error handling improvements.
	
2009-03-03  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/__init__.py:

	Add missing parameter to get_uri_for_path() in the base class.
	
2009-03-02  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/svn.py:

	Add a new method to get the remote uri corresponding to a local
	path where the repository was checked out. 
	
2009-02-21  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* tests/Makefile.am:

	Make tests work again.
	
2009-02-21  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/Command.py:

	Updated from misc. It fixes an error in previous commit.
	
2009-02-20  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/Command.py:

	Update from misc. Standard and error output are not stored in
	variables when using callbacks, saving a lot of memory when
	running commands with very long outputs such as log or diff.
	
2009-02-02  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* configure.in:
	* AUTHORS:
	* NEWS:
	* README:

	Update for release 0.2
	
2009-01-27  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/backends/git.py:

	Do not append uri to log command when it's a directory, since we
	are using it as cwd.
	
2009-01-02  Carlos Garcia Campos  <carlosgc@gsyc.es>

	* repositoryhandler/Command.py:

	Updated from misc.
	
2008-10-14  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Remove the crappy stuff about branches in svn diff when using a
	remote uri.
	
2008-10-13  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:

	Updated from misc

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/svn.py:

	Correctly handle ssl certificate svn error messages providing the
	required input to the svn command.
	
2008-10-07  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/watchers.py:
	* repositoryhandler/backends/bzr.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	* tests/__init__.py:
	* tests/cvs.py:
	* tests/git.py:
	* tests/svn.py:

	Add blame command support. Based on patch by Miguel Angel Tinte
	Garcia.
	
2008-10-07  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/git.py:

	More detailed git log command.
	
2008-09-30  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:

	Update from misc.
	
2008-09-22  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:
	* tests/svn.py:

	Use uri@rev instead of -r rev for checking out in svn backend
	since it works better (ie it's possible to download a removed path
	to its first revision). Thanks to Luis Cañas!
	
2008-09-17  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/bzr.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	* tests/cvs.py:
	* tests/svn.py:

	Add a rlog method to the API to be able to get the log directly
	from the repository. Only supported by cvs and svn.
	
2008-09-16  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:

	Fix get_last_revision for some versions of cvs.
	
2008-09-08  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:
	* tests/cvs.py:

	Implement get_last_revision() in the CVS backend.
	
2008-09-03  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:

	Add a debug option to be able to know what commands are being
	executed by rh.
	
2008-09-03  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:

	Fix update of files in cvs.
	
2008-08-27  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:
	
	Update from misc.
	
2008-07-21  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:

	Remove the -N option from the cvs log command since we are now
	interested in the tag list.
	
2008-07-18  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/git.py:

	Do not use any file path when not provided in git log.
	
2008-07-17  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/bzr.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	* tests/svn.py:

	Remove branch parameter of log method. Do not guess the svn layout
	when checking out, since it causes more problems that it
	solves. Tests have been updated according to the new behaviour. 
	
2008-05-13  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/bzr.py:
	* repositoryhandler/backends/git.py:

	Fix detection of bazar repositories by a path.
	
2008-05-07  Santiago Dueñas Dominguez  <sduenas@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Added parameter to force the update of an uri.
	
2008-05-07  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/Makefile.am:
	* repositoryhandler/backends/bzr.py:
	* tests/Makefile.am:
	* tests/bzr.py:

	Initial bazar support.
	
2008-04-08  Santiago Dueñas Dominguez  <sduenas@gsyc.escet.urjc.es>

	* repositoryhandler/backends/tarball.py:
	
	Delete uri parameters from the destination path

2008-04-08  Santiago Dueñas Dominguez  <sduenas@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	
	Add newdir = '.' as a special case in which rootdir will be the
	full destination of the checkout

2008-04-02  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Make sure uri is the repository root when creating a svn repo.
	
2008-04-02  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:

	Document uri parameter in cvs checkout.
	
2008-03-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* NEWS:

	First release 0.1
	
2008-03-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* Move repositoryhandler to its own module
	
2008-03-13  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Do not run svn co and update with LC_ALL. Fixes bug #407.
	
2008-02-20  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:

	Updated from Misc
	
2008-01-31  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:
	* tests/svn.py:

	Add module = '.' as an special case in svn checkout to be able to
	download the whole repository.
	
2008-01-30  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Makefile.am:
	* repositoryhandler/Downloader.py:
	* repositoryhandler/FindProgram.py:
	* repositoryhandler/backends/tarball.py:

	Use Downloader from misc instead of using directly wget.
	
2008-01-17  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:

	Python2.4 doesn't support keyword arguments in __import__
	
2007-12-04  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Fix svn diff when using a remote uri of a repo without /trunk.
	
2007-12-04  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:

	Add remove_watcher()
	
2007-12-03  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py: Updated from misc
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:

	Use run_sync() instad of run() when needed.
	
2007-11-29  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	* tests/__init__.py:
	* tests/git.py:
	* tests/svn.py:

	Add get_last_revision()
	
2007-11-22  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/git.py:

	Strip git config values before returning them.
	
2007-11-13  Santiago Dueñas Domínguez  <sduenas@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:
	
	Updated from misc.

2007-10-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:

	Update from misc
	
2007-10-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:

	When doing a checkout if srcdir already exists we try to do an
	update instead. If such update fails because srcdir is not a valid
	working copy continue with the chekcout instead of fail.
	
2007-10-08  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:

	Add get_uri()
	
2007-09-27  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Do not consider module/trunk as a module when trunk is not a
	directory.
	
2007-09-27  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py: Update from misc
	* repositoryhandler/backends/svn.py:

	Always pass 'p\n' to stdin when running svn info so that ssl will
	be permanently accepted when needed.
	
2007-09-23  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/git.py:

	Add --pretty=fuller to git log command so that author is shown
	too.
	
2007-09-21  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/git.py:

	Fix git log when uri is a directory and files is None.
	
2007-09-21  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/git.py:
	* repositoryhandler/backends/svn.py:
	* repositoryhandler/backends/tarball.py:
	* tests/tarball.py:

	Add type as an argument of the Repository base class to make sure
	it's always used. Fix tarball test, it used a wrong path.
	
2007-09-21  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/git.py:

	Add -M and -C options to git log command to detect moves and
	copies. 

2007-09-20  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/Makefile.am:
	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/svn.py:
	* repositoryhandler/backends/git.py:
	* tests/Makefile.am:
	* tests/run_test.py.in:
	* tests/git.py:

	Add git support. Diff method is still to be done. 
	
2007-09-19  Santiago Dueñas Domínguez  <sduenas@gsyc.escet.urjc.es>
	
	* repositoryhandler/backends/cvs.py:
	* tests/cvs.py:

	Fixed the download of all the repository' modules
	
2007-09-13  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:
	* tests/svn.py:

	Fix log command when using a svn repository without a /trunk
	directory.
	
2007-09-06  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/tarball.py:
	* tests/tarball.py:

	Add support for gz and bz2 files in tarball backend so that it can
	be used to download and extract mboxes.
	
2007-09-05  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/svn.py:
	* tests/__init__.py:
	* tests/svn.py:

	Add get_modules() method to be able to know the list of modules
	available in repository.
	
2007-08-18  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/svn.py:

	Always run svn command with LC_ALL=C since svn output is
	localized.
	
2007-08-18  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* tests/Makefile.am:
	* tests/run_thread_test.py:
	* tests/run_thread_test.py.in:

	Remove run_thread_test.py since it's a generated file. Use
	run_thread_test.py.in instead.
	
2007-06-29  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/tarball.py:
	* repositoryhandler/backends/svn.py:
	* tests/svn.py:

	Add get_type method to be able to know the repo type of an
	existent instance. Improve remote uri handling in svn backend.
	
2007-06-28  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:
	* repositoryhandler/backends/Makefile.am:
	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/svn.py:
	* repositoryhandler/backends/tarball.py:
	* repositoryhandler/backends/watchers.py:
	* tests/cvs.py:
	* tests/svn.py:

	Rework Command class so that we don't need to wait until process
	is finished in order to process its output. Now a callback can be
	used to process the command output as soon as new output lines are
	available. 

2007-06-14  Israel Herraiz <herraiz@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/svn.py:

	Fixed bug #267. R-H can now checkout, update, log and diff
	individual files.
	
2007-05-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:

	create_repository_from_path needs the list of supported backends. 

	* tests/cvs.py:
	* tests/svn.py:

	Add tests for create_repository_from_path. 

2007-05-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/__init__.py:
	* repositoryhandler/backends/cvs.py:
	* repositoryhandler/backends/svn.py:

	Add a method to create new repositories based on a local path. 

2007-05-24  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/backends/tarball.py:

	Fix a typo. 

2007-05-22  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* tests/Makefile.am:
	* tests/run_thread_test.py:

	Add threads test. 

2007-05-22  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* repositoryhandler/Command.py:

	Fix cvs diff exception in Command. 

2007-05-14  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* Makefile.am:

	Add README file in EXTRA_DIST

2007-03-26  Carlos Garcia Campos  <carlosgc@gsyc.escet.urjc.es>

	* Initial import

