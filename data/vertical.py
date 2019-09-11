# vertical.py
import time
from multiprocess import Pool
from timeit import timeit

def sleeping(arg):
    time.sleep(0.1)
    ncores = 2
    pool = Pool(ncores)
    # sequential run
    %timeit list(map(sleeping, range(24)))
    # parallel run
    %timeit pool.map(sleeping, range(24))
    pool.close()
