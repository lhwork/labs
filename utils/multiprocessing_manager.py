from multiprocessing import Process, Queue, current_process
import time

def f(q):
    name = current_process().name
    config = q.get()
    print "%s got config: %s" % (name, config)
    print "%s beginning processing at %s" % (name, time.asctime())
    time.sleep(5)
    print "%s completing processing at %s" % (name, time.asctime())

if __name__ == '__main__':
    q = Queue()
    processes = []
    cfg = { 'my' : 'config', 'data' : 'here' }
    for i in range(3):
        p = Process(target=f, args=(q,))
        processes.append(p)
        p.start()
        q.put(cfg)

    for p in processes:
        p.join()
