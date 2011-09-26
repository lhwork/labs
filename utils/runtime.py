import time

def Runtime(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print "%s time used: %.3f" % (func.__name__, end - start)
    return wrapper

@Runtime
def test():
    time.sleep(1.2)
    print "test running time."

if __name__ == '__main__':
    test()

