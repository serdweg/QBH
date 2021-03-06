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

# <n_events> <n_extra_dimension> <threshold_mass> <RS_or_PDG> <out_file_name>
paras = [
 [0, 20000, 1, 500, 'RS', 'QBH_n1_RS_500.lhe'],
 [1, 20000, 1, 1000, 'RS', 'QBH_n1_RS_1000.lhe'],
 [2, 20000, 1, 1500, 'RS', 'QBH_n1_RS_1500.lhe'],
 [3, 20000, 1, 2000, 'RS', 'QBH_n1_RS_2000.lhe'],
 [4, 20000, 1, 2500, 'RS', 'QBH_n1_RS_2500.lhe'],
 [5, 20000, 1, 3000, 'RS', 'QBH_n1_RS_3000.lhe'],
 [6, 20000, 1, 3500, 'RS', 'QBH_n1_RS_3500.lhe'],
 [7, 20000, 1, 4000, 'RS', 'QBH_n1_RS_4000.lhe'],
 [8, 20000, 1, 4500, 'RS', 'QBH_n1_RS_4500.lhe'],
 [9, 20000, 1, 5000, 'RS', 'QBH_n1_RS_5000.lhe'],
 [10, 20000, 1, 5500, 'RS', 'QBH_n1_RS_5500.lhe'],
 [11, 20000, 1, 6000, 'RS', 'QBH_n1_RS_6000.lhe'],
 [12, 20000, 1, 6500, 'RS', 'QBH_n1_RS_6500.lhe'],
 # [13, 20000, 2, 500, 'PDG', 'QBH_n2_ADD_500.lhe'],
 # [14, 1000, 2, 1000, 'PDG', 'QBH_n2_ADD_1000.lhe'],
 # [15, 1000, 2, 1500, 'PDG', 'QBH_n2_ADD_1500.lhe'],
 # [16, 1000, 2, 2000, 'PDG', 'QBH_n2_ADD_2000.lhe'],
 # [17, 1000, 2, 2500, 'PDG', 'QBH_n2_ADD_2500.lhe'],
 # [18, 1000, 2, 3000, 'PDG', 'QBH_n2_ADD_3000.lhe'],
 # [19, 1000, 2, 3500, 'PDG', 'QBH_n2_ADD_3500.lhe'],
 # [20, 1000, 2, 4000, 'PDG', 'QBH_n2_ADD_4000.lhe'],
 # [21, 1000, 2, 4500, 'PDG', 'QBH_n2_ADD_4500.lhe'],
 # [22, 1000, 2, 5000, 'PDG', 'QBH_n2_ADD_5000.lhe'],
 # [23, 1000, 2, 5500, 'PDG', 'QBH_n2_ADD_5500.lhe'],
 # [24, 1000, 2, 6000, 'PDG', 'QBH_n2_ADD_6000.lhe'],
 # [25, 1000, 2, 6500, 'PDG', 'QBH_n2_ADD_6500.lhe'],
 [26, 20000, 4, 500, 'PDG', 'QBH_n4_ADD_500.lhe'],
 [27, 20000, 4, 1000, 'PDG', 'QBH_n4_ADD_1000.lhe'],
 [28, 20000, 4, 1500, 'PDG', 'QBH_n4_ADD_1500.lhe'],
 [29, 20000, 4, 2000, 'PDG', 'QBH_n4_ADD_2000.lhe'],
 [30, 20000, 4, 2500, 'PDG', 'QBH_n4_ADD_2500.lhe'],
 [31, 20000, 4, 3000, 'PDG', 'QBH_n4_ADD_3000.lhe'],
 [32, 20000, 4, 3500, 'PDG', 'QBH_n4_ADD_3500.lhe'],
 [33, 20000, 4, 4000, 'PDG', 'QBH_n4_ADD_4000.lhe'],
 [34, 20000, 4, 4500, 'PDG', 'QBH_n4_ADD_4500.lhe'],
 [35, 20000, 4, 5000, 'PDG', 'QBH_n4_ADD_5000.lhe'],
 [36, 20000, 4, 5500, 'PDG', 'QBH_n4_ADD_5500.lhe'],
 [37, 20000, 4, 6000, 'PDG', 'QBH_n4_ADD_6000.lhe'],
 [38, 20000, 4, 6500, 'PDG', 'QBH_n4_ADD_6500.lhe'],
 [39, 20000, 5, 500, 'PDG', 'QBH_n5_ADD_500.lhe'],
 [40, 20000, 5, 1000, 'PDG', 'QBH_n5_ADD_1000.lhe'],
 [41, 20000, 5, 1500, 'PDG', 'QBH_n5_ADD_1500.lhe'],
 [42, 20000, 5, 2000, 'PDG', 'QBH_n5_ADD_2000.lhe'],
 [43, 20000, 5, 2500, 'PDG', 'QBH_n5_ADD_2500.lhe'],
 [44, 20000, 5, 3000, 'PDG', 'QBH_n5_ADD_3000.lhe'],
 [45, 20000, 5, 3500, 'PDG', 'QBH_n5_ADD_3500.lhe'],
 [46, 20000, 5, 4000, 'PDG', 'QBH_n5_ADD_4000.lhe'],
 [47, 20000, 5, 4500, 'PDG', 'QBH_n5_ADD_4500.lhe'],
 [48, 20000, 5, 5000, 'PDG', 'QBH_n5_ADD_5000.lhe'],
 [49, 20000, 5, 5500, 'PDG', 'QBH_n5_ADD_5500.lhe'],
 [50, 20000, 5, 6000, 'PDG', 'QBH_n5_ADD_6000.lhe'],
 [51, 20000, 5, 6500, 'PDG', 'QBH_n5_ADD_6500.lhe'],
 [52, 20000, 6, 500, 'PDG', 'QBH_n6_ADD_500.lhe'],
 [53, 20000, 6, 1000, 'PDG', 'QBH_n6_ADD_1000.lhe'],
 [54, 20000, 6, 1500, 'PDG', 'QBH_n6_ADD_1500.lhe'],
 [55, 20000, 6, 2000, 'PDG', 'QBH_n6_ADD_2000.lhe'],
 [56, 20000, 6, 2500, 'PDG', 'QBH_n6_ADD_2500.lhe'],
 [57, 20000, 6, 3000, 'PDG', 'QBH_n6_ADD_3000.lhe'],
 [58, 20000, 6, 3500, 'PDG', 'QBH_n6_ADD_3500.lhe'],
 [59, 20000, 6, 4000, 'PDG', 'QBH_n6_ADD_4000.lhe'],
 [60, 20000, 6, 4500, 'PDG', 'QBH_n6_ADD_4500.lhe'],
 [61, 20000, 6, 5000, 'PDG', 'QBH_n6_ADD_5000.lhe'],
 [62, 20000, 6, 5500, 'PDG', 'QBH_n6_ADD_5500.lhe'],
 [63, 20000, 6, 6000, 'PDG', 'QBH_n6_ADD_6000.lhe'],
 [64, 20000, 6, 6500, 'PDG', 'QBH_n6_ADD_6500.lhe'],
]

# for item in paras:
    # run_lhe_production_job(item)

pool = multiprocessing.Pool(5)
pool.map_async(run_lhe_production_job, paras)
while True:
    time.sleep(1)
    if not pool._cache: break
pool.close()
pool.join()

print('everything done')
