#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import cPickle as pickle
import struct 
from server import DOMAIN_SOCKET

def test():
    import gevent
    from gevent.pool import Pool
    from gevent import socket

    def flush(idx, domain_socket=DOMAIN_SOCKET):
        data = {"action":"do_%s"%(idx,)}
        msg = pickle.dumps(data)
        msg = struct.pack('!I', len(msg)) + msg

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.connect(domain_socket)
            client.send(msg)
        except:
            import traceback
            traceback.format_exc()

        client.close()


    count = 5
    pool = Pool(count)
    for i in range(count):
        pool.spawn(flush, i, DOMAIN_SOCKET)
    pool.join()

if __name__ == '__main__':
    test()
