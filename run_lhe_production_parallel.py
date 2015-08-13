#!/bin/env python

import subprocess
import multiprocessing
import time
import os

Target = '/disk1/erdweg/QBH/lhes/'
N_events = 10000

def run_lhe_production_job(parameters):
    number = parameters[0]
    print('starting with number %i'%number)

    out_name = parameters[5]

    p = subprocess.Popen('./qbh %i %i %f %s %s'%(parameters[1], parameters[2], parameters[3], parameters[4], out_name),shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    p = subprocess.Popen('mv *%s %s'%(out_name, Target),shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
    out, err = p.communicate()
    print(out)
    print(err)

    print('done with number %i'%number)

paras = [
 [0,100, 1, 500, 'RS', 'QBH_n1_RS_500.lhe'],
 [1,100, 2, 500, 'PDG', 'QBH_n2_ADD_500.lhe'],
]

for item in paras:
    run_lhe_production_job(item)

# pool = multiprocessing.Pool(5)
# pool.map_async(run_lhe_production_job, numbers)
# while True:
    # time.sleep(1)
    # if not pool._cache: break
# pool.close()
# pool.join()

print('everything done')
