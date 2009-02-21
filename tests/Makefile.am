
noinst_SCRIPTS = run_test.py		\
		 run_thread_test.py

tests = __init__.py	\
	bzr.py		\
	cvs.py		\
	git.py		\
	svn.py		\
	tarball.py

EXTRA_DIST = $(tests)			\
	     run_test.py.in		\
	     run_thread_test.py.in

run_test.py: run_test.py.in
	sed -e s!\@testdir\@!$(top_srcdir)! < $< > $@
	chmod a+x $@

run_thread_test.py: run_thread_test.py.in
	sed -e s!\@testdir\@!$(top_srcdir)! < $< > $@
	chmod a+x $@

CLEANFILES = run_test.py		\
	     run_thread_test.py
