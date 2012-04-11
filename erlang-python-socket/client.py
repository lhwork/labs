#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
client.py

Created by 李焕 on 2012-04-11.
Copyright (c) 2012. All rights reserved.
"""

import socket

HOST = 'localhost' # The remote host
PORT = 4444 # The same port as used by the server

def main():
    from gevent.pool import Pool
    from gevent import socket
    
    def send(idx, addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.send("Hello %s, world"%(idx,))
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)
    
    count = 200
    pool = Pool(count)
    for i in range(count):
        pool.spawn(send, i, (HOST, PORT))
    pool.join()

if __name__ == '__main__':
    main()

