#!/usr/bin/python
#Perform Weighted Adjust or Diagonal Adjust
#for i/j in 1...K do
#if i!=j
#qij = arg min(qij[0,c]) || exp(Q(qij)) - P || for some c
#return Q

import numpy as np
import matrixFunctions2d
from scipy.linalg import expm, logm
from scipy import optimize
import sys
c=1
calculations = 0
def distance(q1, q2):#find the distance between the two matrices
   n = q1.shape[0]
   dist = 0.0
   for i in range(n):
      for j in range(n):
#         print i, j, q1[i,j], q2[i,j]
          dist += (q1[i,j] - q2[i,j])**2
   return np.sqrt(dist)

def evaluateHops(hops, i, j, Q):
   P = expm(Q)
   n = Q.shape[0]
   copy = np.copy(Q)
   evaluations = np.zeros(n)
   for k in range(n):
      diff = Q[i,j] - hops[k]
      for u in range(n):
         if(u!=j):
            copy[i,u] += diff

      copy[i,i] = -1 * (np.sum(copy[i,:]) - copy[i,i]) #set diagonal to neg sum
      evaluations[k] = distance(copy, P) #evaluate distance
   return evaluations
def buildHops(n, x, y):
   ar = np.zeros(n)
   step = float((x - y)/n)
   for i in range(n):
      ar[i] = ar[i-1] + step
   return ar
def argmin(i, j, Q, c, epsilon = 0.000000001, maxIters=50):
   value = 1
   n = Q.shape[0]
   tempAr = np.copy(Q[i,:])
   x = 0#min
   y = c#max
   iters = 0
   switch = 0
   while(value>epsilon):
      hops = buildHops(n, x, y)
      evals = evaluateHops(hops, i, j, Q)
      index = np.argmin(evals)
      if(evals[(index+1)%n]>evals[(index-1)%n]):
          value = evals[(index-1)%n] - evals[index]
          x = hops[index]
          y = hops[(index-1)%n]
          if(switch==1):
             y = z
             switch = 0
          else:
             z = hops[index+1]
             switch = 1
      else:
          value = evals[(index+1)%n] - evals[index]
          x = hops[index]
          y = hops[(index+1)%n]
          if(switch==-1):
             y = z
             switch = 0 
          else:
             z = hops[index-1]
             switch = -1
      if(iters>maxIters):
         value =0
      iters +=1
#      print index, value, iters, x, y

   return hops[index] 

mat = matrixFunctions2d.read2dMatrix(sys.argv[1])
mat = matrixFunctions2d.normalize2dMatrix(mat, 0)
P = np.copy(mat) #initial Probability Matrix
mat = logm(mat)
Q = matrixFunctions2d.diagonalAdjustment2d(mat, 0)    #this is our Qnaught
#Q = matrixFunctions2d.weightedAdjustment2d(log)


def func(x,i,j,Q,P):
#    print i,j,x
    Q[i,i] += x - Q[i,j]
    Q[i,j] = x
    return distance(expm(Q), P)


n = Q.shape[0]
q = np.copy(Q) 
for i in range(n):
   for j in range(n):
      if(i!=j):
         if(Q[i,j]>1e-10):
           calculations+=1
           print calculations
           x = optimize.fmin(func, Q[i,j], args=(i,j,Q,P), maxiter=200)[0]#argmin(i, j, Q, c)

           #print "UGH:", Q[i,j],x
         #Q = np.copy(q) #put updated matrix in place of Q
#           Q[i,i] +=x
#           Q[i,i] -= Q[i,j]
           Q[i,j] = x
#   print "Original:\n", Q[i,:], "\nUpdated:\n", q[i,:]
#   if(Q[i,i]!=q[i,i]):
#       quit()
#   quit()
#   Q[i,j] = q[i,j] #put updated matrix in place of Q
#   Q[i,:] = q[i,:]
matrixFunctions2d.write2dMatrix(Q, sys.argv[2])
matrixFunctions2d.writeDetailedBalanceftxt(Q)

