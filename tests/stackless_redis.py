#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import stackless
import redis
import time
import random

#r = redis.Redis(host='localhost', port=6379)

def redis_incr():
    r = redis.Redis(host='localhost', port=6379)
    time.sleep(random.randint(0,5))
    counter = r.incr('c')
    print 'show ',counter
    #stackless.schedule()
    #print 'redis incr end.'

for i in xrange(500):
    stackless.tasklet(redis_incr)()

stackless.run()

