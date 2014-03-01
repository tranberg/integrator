#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division	# Proper division
import matplotlib.pyplot as plt	# For plotting
import numpy as np		# Extra functions
import random			# Pseudo-random numbers
from time import time		# Time measuring
from monte_carlo import *	# Mone Carlo routines
from functions import *		# Catalog of sample functions to be integrated
"""
Definitions
"""
def plotpoints(points):
	"""
	Simple plotting-routine
	"""
	x,y = [],[]
	for i in range(np.shape(points)[0]):
			x.append(points[i][0])
			y.append(points[i][1])
	plt.plot(x, y, ",")
"""
Plain vs. stratified integration of simple circle
"""
a = [-1,-1]
b = [1,1]

#call = np.linspace(1000,100000,100)
call =[1000,5000,10000,100000,1000000]

woop=time()
callings1,qval1,error1,d1,t1 = [],[],[],[],[]
for i in range(len(call)):
	start1 = time()
	calls = call[i]
	points = []
	q,err = plain_monte_carlo(adv_functions().circ,a,b,calls,points)
	callings1.append(calls)
	qval1.append(q)
	error1.append(err)
	d1.append(abs(q-np.pi))
	t1.append(time()-start1)
	if calls == 1000 or calls == 5000 or calls == 10000 or calls == 100000 or calls == 1000000 or calls == 10000000:
		print "Plain Monte Carlo:", calls,"calls","%.5f"%q,"%.5f"%err,"%.5f"%abs(q-np.pi),"in","%.3f"%(time()-start1),"seconds"
callings2,qval2,error2,d2,t2 = [],[],[],[],[]
print "Elapsed so far: ",time()-woop, "seconds"
for i in range(len(call)):
	start1 = time()
	calls = call[i]
	param = [a,b,call[i]]
	points = []
	q,err = rs_monte_carlo(adv_functions().circ, param, points)
	callings2.append(calls)
	qval2.append(q)
	error2.append(err)
	d2.append(abs(q-np.pi))
	t2.append(time()-start1)
	if calls == 1000 or calls == 5000 or calls == 10000 or calls == 100000 or calls == 1000000 or calls == 10000000:
		print "Stratified Monte Carlo:", calls,"calls","%.5f"%q,"%.5f"%err,"%.5f"%abs(q-np.pi),"in","%.3f"%(time()-start1),"seconds"
print "Elapsed so far: ",time()-woop, "seconds"

"""
Plotting of results from above
"""
#plt.plot(callings1,d1,'-b')
#plt.plot(callings2,d2,'-k')
#plt.legend(('Plain','Stratified'),loc='best')
#plt.title('Deviation from pi compared to number of calls')
#plt.savefig('dev_call.png',format='png')

"""
Plot to compare types of sampling
"""
start2 = time()
param = [a,b,50000]
points = []
print "Stratified Monte Carlo", rs_monte_carlo(adv_functions().circ,param, points),"in","%.2f"%(time()-start2),"seconds"
plt.figure(figsize=(10,10))
x1 = np.linspace(-1, 1, 500)
y1 = np.sqrt(1-x1**2)
y2 = -1*y1
plt.plot(x1, y1, "r-", lw=2)
plt.plot(x1, y2, "r-", lw=2)
plotpoints(points)

plt.savefig("circle_strat_monte.png",format='png')

start2 = time()
points = []
print "Plain Monte Carlo", plain_monte_carlo(adv_functions().circ, a, b, 50000, points),"in","%.2f"%(time()-start2),"seconds"
plt.figure(figsize=(10,10))
x1 = np.linspace(-1, 1, 500)
y1 = np.sqrt(1-x1**2)
y2 = -1*y1
plt.plot(x1, y1, "r-", lw=2)
plt.plot(x1, y2, "r-", lw=2)
plotpoints(points)
plt.savefig("circle_monte.png",format='png')

print "Elapsed so far: ",time()-woop, "seconds"
"""
Data for comparison between one CPU and multiple CPUs
"""
print "\n3 stratified calculations to be compared to multi-processing\n"
a = [-1,-1]
b = [1,1]

call =[100000,1000000,10000000]

callings1,qval1,error1,d1,t1 = [],[],[],[],[]
for i in range(len(call)):
	start1 = time()
	calls = call[i]
	points = []
	q,err = plain_monte_carlo(adv_functions().circ,a,b,calls,points)
	callings1.append(calls)
	qval1.append(q)
	error1.append(err)
	d1.append(abs(q-np.pi))
	t1.append(time()-start1)
	print "Plain Monte Carlo:", calls,"calls","%.5f"%q,"%.7f"%err,"%.7f"%abs(q-np.pi),"in","%.3f"%(time()-start1),"seconds"
print "Elapsed so far: ",time()-woop, "seconds"
