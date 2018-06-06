#!/usr/bin/python
import numpy as np
import scipy.integrate as integrate
from scipy.linalg import expm, logm, inv
import matrixFunctions2d
#helper file for calculating EM algorithm
def makeOneHotVector(i, n):
   matrix = np.zeros(n)
   matrix[i] = 1
   return matrix

def integrand(s, Q, i, j):
   n = Q.shape[0]
   pro1 = np.matmul(expm((1-s)*Q), makeOneHotVector(i,n))
   pro2 = np.matmul(np.transpose(makeOneHotVector(j,n)),expm(s*Q))
   pro3 = np.matmul(pro1, np.transpose(pro2))
   return pro3

def calcF_1_2(Q, i, j):
   n = Q.shape[0]
   result, _ = integrate.quad(integrand, 0, 1, args=(Q,i,j))
#   result = integrate.romberg(integrand, 0, 1, args=(Q,i,j))

#   result, _ = integrate.quad(integrand, -1, 0, args=(Q,i,j))
#   return -1.0 * result
   return result

def expectation(Q,i,j):
   n = Q.shape[0]
#I think this cancels for the qij values   Dinv = inv(expm(Q))#nxn matrix
   integrand = calcF_1_2(Q,i,j)#NxN matrix
   if(i==j):
      return integrand
   else:
      return Q[i,j] * integrand

def frobenius(q1, q2):#find the 'distance' between two matrices
   n = q1.shape[0]
   dist = 0.0
   for i in range(n):
      for j in range(n):
         dist += (q1[i,j] - q2[i,j])**2
   return np.sqrt(dist)

def nextTimeStep(Q, epsilon):#returns the next timestep and a 0 to continue loop, or the same value and a 1 to stop the loop
   n = Q.shape[0]
   NextQ = np.zeros((n,n))
   for i in range(n):
      for j in range(n):
         NextQ[i,j] = expectation(Q,i,j)#as defined in paper, see above functions
   NextQN = matrixFunctions2d.normalize2dMatrix(NextQ)
#Cannot be weighted adjust, investigate why later   NextQ = matrixFunctions2d.weightedAdjustment2d(NextQN)
   NextQ = matrixFunctions2d.diagonalAdjustment2d(NextQN)

#   print NextQ
   dist = frobenius(NextQ,Q)
   if(dist<epsilon):
      return Q, dist, 1
   else:
      return NextQ, dist,  0
         

#Q = np.zeros((5,5))

#Q[0,:] = 1
#Q[1,:] = 2
#Q[2,:] = 3
#Q[3,:] = 4
#Q[4,:] = 5
#expectation(Q,3,2)
