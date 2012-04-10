#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cPickle as pickle
import struct
from errno import ENOENT, EAGAIN, EWOULDBLOCK, EINTR

from daemon import Daemon

_DEBUG = True

DOMAIN_SOCKET = '/tmp/.service.sock'

def unlink(path):
    '''unlink the specified file path
    '''
    import os
    try:
        os.unlink(path)
    except OSError, ex:
        if ex.errno != ENOENT:
            raise

def link(src, dest):    
    '''link the specified file path
    '''
    import os
    try:
        os.link(src, dest)
    except OSError, ex:
        if ex.errno != ENOENT:
            raise

def bind_unix_listener(path, backlog=50, user=None):
    '''Create socket which will bind & listen one unix domain socket.
       The file ownership and permission will also be set if argument user is specified.
    '''
    import _socket
    import os
    import pwd

    pid = os.getpid()
    tempname = '%s.%s.tmp' % (path, pid)
    backname = '%s.%s.bak' % (path, pid)
    unlink(tempname)
    unlink(backname)
    link(path, backname)
    try:
        sock = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
        sock.setblocking(0)
        sock.bind(tempname)
        try:

            if user is not None:
                user = pwd.getpwnam(user)
                os.chown(tempname, user.pw_uid, user.pw_gid)
                os.chmod(tempname, 0600)
            sock.listen(backlog)
            try:
                os.rename(tempname, path)
            except:
                os.rename(backname, path)
                backname = None
                raise
            tempname = None
            return sock
        finally:
            if tempname is not None:
                unlink(tempname)
    finally:
        if backname is not None:
            unlink(backname)

def handler(sock, address):
    '''Socket handler.
       Data will be read out from the soket, and push request into proper queue.
    '''

    msg = ''

    while True:

        try:
            tmp = sock.recv(4096)
        except OSError, ex:
            if ex.errno == EINTR:
                pass
            elif ex.errno == EAGAIN or ex.errno == EWOULDBLOCK:
                break
            else:
                try:
                    sock.close()
                finally:
                    return

        if len(tmp) > 0:
            msg += tmp

            while len(msg) >= 4:
                try:
                    rc = struct.unpack("!I", msg[:4])
                    i = rc[0]
                except Exception,e:
                    print e
                    break

                if i == 0:
                    msg = msg[4:]
                else:
                    # i > 0
                    i += 4
                    if len(msg) >= i:
                        print(pickle.loads(msg[4:i]))
                        msg = msg[i:]
                    else:
                        break
                
            pass   # keep it looping

        else:
            sock.close()
            return

class service(Daemon):

    def run(self):
        from gevent import monkey; monkey.patch_socket()
        from gevent.server import StreamServer
    
        domain_socket = DOMAIN_SOCKET
        StreamServer(bind_unix_listener(domain_socket), handler).serve_forever()

if __name__ == '__main__':
    daemon = service("./service.pid")
    import sys
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(1)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

