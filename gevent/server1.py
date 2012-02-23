import gevent
from gevent.server import StreamServer

def eat_cpu():
    for i in xrange(10000): pass

def cb(socket, address):
    eat_cpu()
    socket.recv(1024)
    socket.sendall('HTTP/1.1 200 OK\n\nHello World!!')
    socket.close()

server = StreamServer(('',8000), cb, backlog=100000)
server.pre_start()

gevent.fork()

server.start_accepting()
server._stopped_event.wait()
