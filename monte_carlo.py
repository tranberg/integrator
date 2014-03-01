#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import random
import numpy as np
from itertools import izip

"""
Main program
"""
def plain_monte_carlo(fun,a,b,N,points):
	"""
	Plain Monte Carlo integrator
	"""
	sum1,sum2 = 0,0
	V = 1			# Integration volume
	for i in range(len(a)):
		V *= (b[i]-a[i])
	for i in range(N):
		x = [a[i]+random.random()*(b[i]-a[i]) for i in range(len(a))]
		points.append(x)# Sampled points to be plotted
		f = fun(*x)
		sum1 += f
		sum2 += f**2
	avg = sum1/N		# Average
	var = sum2/N-avg**2	# Variance
	q = V*avg		# Integral value
	err = V*np.sqrt(var/N)	# Error
	return q,err

def rs_monte_carlo(function,param,points,R='None'):
	"""
	Recursive stratified Monte Carlo integrator
	"""
	# The purpose of R is multiprocessing
	# If we are multiprocessing: R !== 'None'
	if R == 'None':			# If not multiprocessing
		a = param[0]
		b = param[1]
		calls = param[2]
	else:
		a,b,calls = param.get() # If multiprocessing

	dim = len(a)			# Number of dimensions
	est_calls = calls//10		# Allocating 10% the calls
	min_calls = 3

	if est_calls < dim*16 or (calls-est_calls < 2*min_calls):
		q,err = plain_monte_carlo(function,a,b,calls,points)
		if R != 'None':
			R.put([q,err])	# If multiprocessing
		else:
			return q,err	# If not multiprocessing

	# Estimate variances of subregions
	q, variance, vars_low, vars_up = ebv(function, a, b, est_calls, points)

	calls -= est_calls + 2*min_calls

	min_var = 1000000.
	axis = 0
	for i, (v_low, v_up) in enumerate(izip(vars_low, vars_up)):
		s_low = np.sqrt(v_low)
		s_up = np.sqrt(v_up)
		var = s_low**(1/3) + s_up**(1/3)
		if var <= min_var:
			min_var = var
			axis = i
			weight_low = s_low**(1/3) if s_low else 0.
			weight_up = s_up**(1/3) if s_up else 0.
	
	# Here we calculate new bounds
	b1 = b[:]
	b1[axis] = a[axis] + (b[axis]-a[axis])/2
	a2 = a[:]
	a2[axis] = b1[axis]
	
	if weight_low or weight_up:	
		calls_low = min_calls + int(calls*weight_low/(weight_low+weight_up))
		calls_up = 2*min_calls + calls - calls_low
	else:
		calls_low = min_calls + calls//2
		calls_up = 2*min_calls + calls - calls_low
	
	# Here we make two recursive calls
	param1 = [a,b1,calls_low]
	param2 = [a2,b,calls_up]
	value1, error1 = rs_monte_carlo(function, param1, points)
	value2, error2 = rs_monte_carlo(function, param2, points)

	# Returning integral plus error
	q = value1+value2
	err = np.sqrt(error1**2+error2**2)
	if R != 'None':
		R.put([q,err])	# If multiprocessing
	else:
		return q,err	# If not multiprocessing
"""
Definitions
"""
class variancec(object):
	"""
	Variance calculator
	"""
	def __init__(self):
		self.sum = 0.
		self.square_sum = 0.
		self.num = 0.
	def push_value(self, value):
		self.sum += value
		self.square_sum += value**2
		self.num += 1
	def __call__(self):
		return self.square_sum/self.num - (self.sum/self.num)**2
def call(function):
	return function()
def ebv(function, a, b, calls, points):
	"""
	Estimate variances of subregions
	"""
	dim = len(a)
	m2,mean = 0.,0.
	
	up_vars = [variancec() for _ in range(dim)]
	low_vars = [variancec() for _ in range(dim)]

	ranges = [b[i] - a[i] for i in range(dim)]
	half = [a[i] + ranges[i] / 2 for i in range(dim)]
	V = 1
	for i in range(dim):
		V *= ranges[i]
	for n in range(calls):
		x = [0]*dim
		j = (n//2) % dim
		side = n % 2
		for i in range(dim):
			r = random.random()
			if i != j:
				x[i] = a[i] + r * ranges[i]
			else:
				if side == 0:
					x[i] = half[i] + r * ranges[i] / 2
				else:					
					x[i] = a[i] + r * ranges[i] / 2
		points.append(x)
		f = function(*x)
		for i in range(dim):
			if x[i] < half[i]:
				low_vars[i].push_value(f)
			else:
				up_vars[i].push_value(f)
		delta = f - mean
		mean += delta/(n+1)
		m2 += delta * (f - mean)
	q = V*mean
	variance = m2/(n - 1)
	return q, variance, map(call, low_vars), map(call, up_vars)
