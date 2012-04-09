#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import threading
import redis
import time
import random

def redis_incr():
    r = redis.Redis(host='localhost', port=6379)
    time.sleep(random.randint(0,5))
    counter = r.incr('c')
    print 'show ',counter

if __name__ == '__main__':
    threads = []
    for i in xrange(500):
        threads.append(threading.Thread(target=redis_incr))

    for t in threads:
        t.start()

    for t in threads:
        t.join()


