#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os

define("port", default=7777, help="Run server on a specific port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("Info")
        self.write("Running")

class LogStreamer(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        interval_ms = 1000
        try:
            filename = "/var/log/system.log"
            self.file = open(filename, "r")
            self.file.seek(os.stat(filename)[6])
            self.main_loop = tornado.ioloop.IOLoop.instance()
            self.scheduler = tornado.ioloop.PeriodicCallback(self.async_callback(self.go), interval_ms, io_loop=self.main_loop)
            #start your period timer
            logging.info("Scheduler started")
            self.scheduler.start()

        except Exception, e:
            logging.error("Exception in LogStreamer: ", exc_info=True)

    def go(self):
        if self.request.connection.stream.closed():
            logging.debug("Client gone....")
            logging.debug("Stopping scheduler")
            self.scheduler.stop()
            self.scheduler = None
            return
        else:
            logging.debug("Returning to client")
            while True:
                line = self.file.readline()
                if not line:
                    return
                else:
                    self.write(line + "<br/>")
                    self.flush()



application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/tail", LogStreamer)
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    tornado.options.parse_command_line()
    http_server.listen(options.port)
    logging.info("TornadoLog started. Point your browser to http://localhost:%d/tail" % options.port)
    tornado.ioloop.IOLoop.instance().start()

