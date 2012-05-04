import multiprocessing
import time

def do_calculation(data):
    time.sleep(10)
    return data*2
def start_process():
    print 'Starting',multiprocessing.current_process().name

if __name__=='__main__':
    inputs=list(range(100000))
#    print 'Inputs  :',inputs

    start_time = time.time()
    #builtin_output=map(do_calculation,inputs)
    end_time = time.time()
    print 'Run time :', end_time - start_time
    #print 'Build-In :', builtin_output

    pool_size=multiprocessing.cpu_count()*2
    pool=multiprocessing.Pool(processes=pool_size,
        initializer=start_process,)

    start_time = time.time()
    pool_outputs=pool.map(do_calculation,inputs)
    pool.close()
    pool.join()
    end_time = time.time()

    print 'Pool Run time :', end_time - start_time

    #print 'Pool  :',pool_outputs
