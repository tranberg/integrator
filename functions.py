#/usr/bin/python

from __future__ import division
import numpy as np

"""
Sample functions for use with Monte Carlo integrators
"""

class simple_functions:
	def f1(self,x):
		f = 1/((1-np.cos(x[0])*np.cos(x[1])*np.cos(x[2]))*np.pi**3)
		return f
	def f2(self,x):
		f = np.cos(x[0])*np.sin(x[1])
		return f
class adv_functions:
	def circ(self,x,y):
		if x**2+y**2 < 1:
			return 1
		else:
			return 0

    def adv_circ(self,x,y):
        if x**2+y**2 > 1 and ..."not finished" :
            return 1
        else:
            return 0
