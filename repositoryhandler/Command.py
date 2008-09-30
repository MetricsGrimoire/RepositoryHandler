# Command.py
#
# Copyright (C) 2007 Carlos Garcia Campos <carlosgc@gsyc.escet.urjc.es>
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
import select
import subprocess
import sys
import errno
from signal import SIGINT

class CommandError (Exception):

    def __init__ (self, msg, returncode = None):
        Exception.__init__ (self, msg)
        self.returncode = returncode

class Command:

    def __init__ (self, command, cwd = None, env = None):
        self.cmd = command
        self.cwd = cwd
        self.env = env

    def run_sync (self, stdin = None):
        kws = { 'close_fds': True,
                'stdout'   : subprocess.PIPE,
                'stderr'   : subprocess.PIPE,
                'env'      : os.environ.copy ()
        }

        if self.cwd is not None:
            kws['cwd'] = self.cwd

        if self.env is not None:
            kws['env'].update (self.env)

        try:
            return subprocess.Popen (self.cmd, **kws).communicate (stdin)[0]
        except OSError, e:
            raise CommandError (str (e))
        
        return None
        
    def run (self, parser_out_func = None, parser_error_func = None):
        def _read (fd, buffsize):
            while True:
                try:
                    return os.read (fd, buffsize)
                except OSError, e:
                    if e.errno == errno.EINTR:
                        continue
                    else:
                        raise
                    
        kws = { 'close_fds': True,
                'stdout'   : subprocess.PIPE,
                'stderr'   : subprocess.PIPE,
                'env'      : os.environ.copy ()
        }

        if self.cwd is not None:
            kws['cwd'] = self.cwd

        if self.env is not None:
            kws['env'].update (self.env)

        try:
            p = subprocess.Popen (self.cmd, **kws)
        except OSError, e:
            raise CommandError (str (e))

        read_set = [p.stdout, p.stderr]
        
        out_data = err_data = ""
        try:
            while read_set:
                try:
                    rlist, wlist, xlist = select.select (read_set, [], [])
                except select.error, e:
                    # Ignore interrupted system call, reraise anything else
                    if e.args[0] == errno.EINTR:
                        continue
                    raise

                if p.stdout in rlist:
                    out_chunk = _read (p.stdout.fileno (), 1024)
                    if out_chunk == "":
                        p.stdout.close ()
                        read_set.remove (p.stdout)
                    out_data += out_chunk
                    
                    while '\n' in out_data:
                        pos = out_data.find ('\n')
                        if parser_out_func is not None:
                            parser_out_func (out_data[:pos + 1])
                        else:
                            sys.stdout.write (out_data[:pos + 1])
                        out_data = out_data[pos + 1:]
        
                if p.stderr in rlist:
                    err_chunk = _read (p.stderr.fileno (), 1024)
                    
                    if err_chunk == "":
                        p.stderr.close ()
                        read_set.remove (p.stderr)
                    err_data += err_chunk
                    
                    while '\n' in err_data:
                        pos = err_data.find ('\n')
                        if parser_error_func is not None:
                           parser_error_func (err_data[:pos + 1])
                        else:
                            sys.stderr.write (err_data[:pos + 1])
                        err_data = err_data[pos + 1:]

        except KeyboardInterrupt:
            try:
                os.kill (p.pid, SIGINT)
            except OSError:
                pass

        ret = p.wait ()
        # If cvs is successful, it returns a successful status; if there is an error, 
        # it prints an error message and returns  a  failure  status. The  one
        # exception  to this is the cvs diff command.  It will return a successful status 
        # if it found no differences, or a failure status if there were differences or if 
        # there was an error.  Because this behavior provides no good way to detect errors, 
        # in the future it is possible that cvs  diff  will be changed to behave like 
        # the other cvs commands.
        if ret == 0 or (self.cmd[0] == 'cvs' and self.cmd[5] == 'diff'):
            return
        
        raise CommandError ('Error running %s' % self.cmd, p.returncode)

if __name__ == '__main__':
    # Valid command without cwd
    cmd = Command (['ls', '-l'])
    cmd.run ()

    # Valid command with cwd
    cmd = Command (['ls', '-lh'], '/')
    cmd.run ()

    # Invalid command
    cmd = Command ('invalid')
    try:
        cmd.run ()
    except CommandError, e:
        print 'Command not found (%s)' % (str (e))

    # Run sync
    cmd = Command (['ls'], '/tmp/')
    print cmd.run_sync ()    


