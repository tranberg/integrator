#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import random
from time import time
from monte_carlo import *
from functions import *
import multiprocessing as mp

start1 = time()

calls = 10000000

# When using 4 CPUs
# a = ([[-1,-1],[0,1],[-1,0],[0,1]])
# b = ([[0,0],[-1,0],[0,1],[0,1]])

# When using 2 CPUs
a = ([[-1,-1],[-1,0]])
b = ([[1,0],[1,1]])
	
tasks = 2 # mp.cpu_count() # use number of avaiable CPUs
destask = tasks

bound = mp.Queue()
Res = mp.Queue()
points = []
proc = [mp.Process(target = rs_monte_carlo, \
		args = (adv_functions().circ,bound,points,Res)) for i in range(tasks)]
for i in proc:
	i.start()
for i in range(tasks):
	aa = a[i]
	bb = b[i]
	N = calls/tasks
	bound.put([aa,bb,N])
#for i in proc:
#	i.join()
q,err = 0,0
while tasks:
	qp,errp = Res.get()
	q += qp
	err += errp
	tasks -= 1
elapsed1 = time()-start1
print "Unit circle integration on ",destask," CPUs with ",calls," points in each section\n"
print "q: ",q,"\ndelta(pi):",abs(q-np.pi),"\nerr: ",err,"\nIn ""%.4f"%elapsed1, "seconds"
