# -*- coding: UTF-8 -*-
import threading
import urllib

class HttpPool():

    def __init__(self):
        self.workers = []
        self.lock = threading.Lock()

    def add(self, url, callback=None, args=()):
        lock = self.lock

        def asynHttpRequest(*args, **opt):
            result = urllib.urlopen(url)
            data = result.read()

            retry = opt.get("retry", 0)
            if not data and retry < 5:
                retry += 1
                return asynHttpRequest(*args, retry=retry)

            lock.acquire()

            if callback:
                callback({
                    "url": url,
                    "data": data
                }, *args)

            lock.release()

        self.workers.append(
            threading.Thread(target=asynHttpRequest, args=args)
        )

    def send(self):
        for w in self.workers:
            w.start()
        for w in self.workers:
            w.join()
        self.onComplete()

    def onComplete(self):
        pass

def parseInfo(res, *args):
    print res, args

if __name__ == '__main__':
    pool = HttpPool()
    pool.add('http://www.vim.org/', callback=parseInfo, args=({'test':'1234'},))
    pool.send()



