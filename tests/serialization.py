#!/usr/bin/env python

# Average runs looks like this:
# $ ./serialization.py 
# Starting json...
# done: 5.75292301178
# Starting simplejson...
# done: 6.66689586639
# Starting cjson...
# done: 2.09307098389
# Starting pickle...
# done: 6.19903492928

import time
import cPickle as pickle
import simplejson
import json
import cjson
import wbin
import demjson


d = {
    'foo': 'bar',
    'food': 'barf',
    'good': 'bars',
    'dood': 'wheres your car?',
    'wheres your car': 'dude?',
}

print 'Starting json...'
print json.dumps(d)
print len(json.dumps(d))
start = time.time()
for i in xrange(1000000):
    json.dumps(d)
print 'done:', time.time() - start

print 'Starting simplejson...'
print simplejson.dumps(d)
print len(simplejson.dumps(d))
start = time.time()
for i in xrange(1000000):
    simplejson.dumps(d)
print 'done:', time.time() - start

print 'Starting cjson...'
print cjson.encode(d)
print len(cjson.encode(d))
start = time.time()
for i in xrange(1000000):
    cjson.encode(d)
print 'done:', time.time() - start

print 'Starting pickle 0 ...'
print pickle.dumps(d)
print len(pickle.dumps(d))
start = time.time()
for i in xrange(1000000):
    pickle.dumps(d)
print 'done:', time.time() - start

print 'Starting pickle 1 ...'
print pickle.dumps(d, 1)
print len(pickle.dumps(d, 1))
start = time.time()
for i in xrange(1000000):
    pickle.dumps(d, 1)
print 'done:', time.time() - start

print 'Starting pickle 2 ...'
print pickle.dumps(d, 2)
print len(pickle.dumps(d, 2))
start = time.time()
for i in xrange(1000000):
    pickle.dumps(d, 2)
print 'done:', time.time() - start

print 'Starting wbin...'
print wbin.serialize(d)
print len(wbin.serialize(d))
start = time.time()
for i in xrange(1000000):
    wbin.serialize(d)
print 'done:', time.time() - start

#print 'Starting demjson...'
#print demjson.encode(d)
#print len(demjson.encode(d))
#start = time.time()
#for i in xrange(1000000):
#    demjson.encode(d)
#print 'done:', time.time() - start

