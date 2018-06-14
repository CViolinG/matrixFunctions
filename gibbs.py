#!/usr/bin/python

import matrixFunctions2d
import metropolis
import numpy as np
from scipy.linalg import logm, expm
import random
import sys
import math
import EMHelper
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

#generate alpha matrix using an EM, set alpha[i,j] = 1 if EM[i,j]>1e-14 else alpha[i,j]=0
#code from expectationMaximization.py
logd = logm(distribution)
diag = matrixFunctions2d.diagonalAdjustment2d(logd)
epsilon = 0.0001
i=0
maxIters=200
exit=0
maxiters=200
while(exit==0):
   diag, dist, exit = EMHelper.nextTimeStep(diag, epsilon)
   i+=1
   print i, dist
   if(i==maxIters):
      print "Maximum Iterations Reached: %s"%i
      print "Exiting EM Portion of sampler"
      exit=1
########### copied code end ##########
alpha = np.zeros((n,n))
for i in range(n):
   for j in range(n):
      if(diag[i,j]<0.00000000000001):
         alpha[i,j] = 0
      else:
         alpha[i,j] = 1

val = 0.00000000000000001
print "Alpha"
for i in range(n):
   for j in range(n):
      if(j!=i):
         Q[i,j] = gammaFunction(val,val, alpha[i,j])
      print alpha[i,j],
   print "Q"
for i in range(n):#set diagonals
   Q[i,i] = -1 * np.sum(Q[i,:]) - Q[i,i]
   for j in range(n):
      print Q[i,j],
   print
#Gibbs Sampler with metropolis-hastings to create draws
nGibbs = int(sys.argv[2]) 
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
         if(N[i,j] == 0):
            N[i,j] = val
         Q[i,j] = gammaFunction(N[i,i], N[i,j], alpha[i,j])#Use Samples to make new Q
   for i in range(n):
      Q[i,i] = np.sum(Q[i,:]) - Q[i,i] 
   #repeat





   matrixFunctions2d.write2dMatrix(N, "gibbs_matrix_%s_%s.dat"%(sys.argv[1], totalIters-nGibbs))
   matrixFunctions2d.printDetailedBalanceftxt(N, "gibbs_db_%s_%s.dat"%(sys.argv[1], totalIters-nGibbs), "Number of Iterations : %s\n"%sys.argv[2])
#   counts = metropolis.countSamples(samples, n)
#   metropolis.printCounts(fname, totalCount, accepted, n, counts, xval)
   

