# -*- coding: UTF-8 -*-
import sys
from chat_service import chatservice

def test():
    import gevent
    from gevent.pool import Pool
    from gevent import socket

    def robot(idx, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        data = {"name":"user%s"%(idx,)}
        chatservice.connect(sock, data)
        while True:
            msg = {"cmd" : "sendmsg", "msg" : "hallo from %s" % (idx,)}
            chatservice.sendmsg(sock, msg)
            gevent.sleep(3)

    host = sys.argv[1]
    port = int(sys.argv[2])
    count = 5000
    pool = Pool(count)
    for i in range(count):
        pool.spawn(robot, i, host, port)
    pool.join()

if __name__ == '__main__':
    test()
