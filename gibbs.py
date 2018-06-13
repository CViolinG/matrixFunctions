#!/usr/bin/python

import matrixFunctions2d
import metropolis
import numpy as np
from scipy.linalg import logm, expm
import random
import sys
import math

#def gammaFunction(R, N, alpha=1, beta=1):
#   x = random.random()
#   beta = (beta + R)**-1
#   alpha = alpha + N
#
#   if(beta<=0 or alpha <1):
#      print "invalid value found in gamma function"
#      quit()
#
#   t1 = beta ** alpha
#   t2 = x ** (alpha - 1)
#   t3 = np.exp(-1.0 * beta * x)
#   t4 = math.factorial(int(alpha - 1))
#
#   return t1 * t2 * t3 / t4

def gammaFunction(R, N, alpha=1, beta=1):
   beta += R
   beta = 1 / beta
   alpha += N 
   return np.random.gamma(alpha, beta, 1)


##################initialize sampling
#read in distribution to match
fname = sys.argv[1]
MATRIX = matrixFunctions2d.read2dMatrix(fname)
distribution = matrixFunctions2d.normalize2dMatrix(MATRIX,0)#normalize along rows
n = MATRIX.shape[0]
#make random initial generator matrix
Q = np.zeros_like(MATRIX)
for i in range(n):
   for j in range(n):
      Q[i,j] = gammaFunction(0,0)

#Gibbs Sampler with metropolis-hastings to create draws
nGibbs = 4 
totalIters = nGibbs
xval = 4
niters = 1000
deltaT = 1#number of times to jump through prior before moving to next step
repeats = 100  
while(nGibbs>0):
   print "Gibbs Iteration: ", totalIters-nGibbs
   nGibbs -= 1
   samples, accepted, totalCount = metropolis.metropolisHastings(niters, repeats, n, distribution, deltaT, metropolis.transitionProbSimple, metropolis.stepGenerator, Q)#Draw Samples Using Q
   N = metropolis.samplesToN(samples, n)
   N = matrixFunctions2d.normalize2dMatrix(N,0)#normalize along row
   for i in range(n):
      for j in range(n):
         Q[i,j] = gammaFunction(N[i,i], N[i,j])#Use Samples to make new Q
   for i in range(n):
      Q[i,i] = np.sum(Q[i,:]) - Q[i,i] 
   #repeat





   matrixFunctions2d.write2dMatrix(N, "gibbs_matrix_%s_%s.txt"%(sys.argv[1], totalIters-nGibbs))
   matrixFunctions2d.printDetailedBalanceftxt(N, "gibbs_db_%s_%s.txt"%(sys.argv[1], totalIters-nGibbs))
   counts = metropolis.countSamples(samples, n)
   metropolis.printCounts(fname, totalCount, accepted, n, counts, xval)
   

