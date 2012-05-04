#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import redis

client = redis.Redis(host = 'localhost', port = 6379)
client.set('test', 0)

def test():
    from gevent.pool import Pool

    def incr(idx):
        print idx
        with client.pipeline() as pipe:
            pipe.watch('test')
            val = int(pipe.get('test'))
            val += 1
            pipe.multi()
            pipe.set('test', val)

            ret = pipe.execute()
            print ret

    count = 5
    pool = Pool(count)
    for i in range(count):
        pool.spawn(incr, i)
    pool.join()

if __name__ == '__main__':
    for i in range(10):
        test()
