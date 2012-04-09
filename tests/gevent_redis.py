#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gevent
import redis
import random


def redis_incr(pid):
    r = redis.Redis(host='localhost', port=6379)
    gevent.sleep(random.randint(0,2))
    print 'Redis', pid, 'done'
    counter = r.incr('c')
    print 'show ', counter

def run():
    threads = []
    for i in range(500):
        threads.append(gevent.spawn(redis_incr, i))
    gevent.joinall(threads)

if __name__ == '__main__':
    run()

