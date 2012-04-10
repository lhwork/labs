#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import struct
import cPickle as pickle
from gevent import monkey; monkey.patch_all();
from gevent.server import StreamServer

class Protocol:
    Connect = 'connect'
    SendMsg = 'sendmsg'
    Quit = 'quit'

    
def gen_pro_data(msg):
    d_data = pickle.dumps(msg)
    d_data = struct.pack('!I', len(d_data)) + d_data
    return d_data

def parse_pro_data(data):
    return pickle.loads(data)

class ChatService:
    def __init__(self):
        self._clients = {}
        self._handlers = {
            Protocol.Connect : self.connect,
            Protocol.SendMsg : self.sendmsg,
            Protocol.Quit : self.quit,
        }

    def connect(self, sock, data):
        userinfo = self._clients.get(sock, None)
        if userinfo: return
        self._clients[sock] = data['name']
        print "New User : %s" % (data['name'],)

    def sendmsg(self, sock, data):
        msg = gen_pro_data(data)
        for s, u in self._clients.items():
            if sock != s:
                s.send(msg)

    def quit(self, sock, data=None):
        if sock in self._clients:
            print "User [%s] quit." % (self._clients[sock],)
            del self._clients[sock]
            sock.close()

    def process(self, sock, promsg):
        cmd = promsg['cmd']
        func = self._handlers[cmd]
        func(sock, promsg)

chatservice = ChatService()

def serve(sock, addr):
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
                        content = msg[4:i]
                        print parse_pro_data(content)
                        #chatservice.process(sock, parse_pro_data(content))
                        msg = msg[i:]
                    else:
                        break
            pass   # keep it looping
        else:
            #chatservice.quit(sock)
            sock.close()
            return

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    print "Start chat server on %s:%s" % (host, port)
    try:
        chatserver = StreamServer((host, port), serve)
        chatserver.serve_forever()
    except:
        chatserver.kill()
