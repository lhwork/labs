#!/usr/bin/env python
#-*- coding:utf-8 -*-
import multiprocessing
import os
import sys
import Queue

def writeQ(q,obj):
    q.put(obj,True,None)
    #print "put size: ",q.qsize()
    
def readQ(q):
    ret = q.get(True,1)
    #print "get size: ",q.qsize()
    return ret
    
def producer(q):
    pid = os.getpid()
    handle_file = 'uid.txt'
    with open(handle_file,'r') as f:
        for line in f:
            print "producer <" ,pid , "> is doing: ",line
            writeQ(q,line.strip())
        q.close()
        
def worker(q):
    pid = os.getpid()
    empty_count = 0
    while True:
        try:
            task = readQ(q)
            print "worker <" , pid , "> is doing: " ,task
        except Queue.Empty:
            empty_count += 1
            if empty_count == 3:
                print "queue is empty, quit"
                q.close()
                sys.exit(0)
                
def main():
    concurrence = 3
    q = multiprocessing.Queue(10)
    funcs = [producer , worker]
    for i in range(concurrence-1):
        funcs.append(worker)
    nfuncs = range( len(funcs) )
    processes = []
    for i in nfuncs:
        p = multiprocessing.Process(target=funcs[i] , args=(q,))
        processes.append(p)
    print "concurrence worker is : ",concurrence," working start"
    for i in nfuncs:
        processes[i].start()
    for i in nfuncs:
        processes[i].join()
    print "all DONE"
    
if __name__ == '__main__':
    main()

