#!/usr/bin/python
import numpy as np
from scipy.linalg import logm, expm
import math
import random
import matrixFunctions2d

def posteriorQ(matrix, N, alpha, beta):
   n = matrix.shape[0]
   R = np.zeros(n)
   mat = np.copy(matrix)
   for i in range(n):
      R[i] = matrix[i,i]
   print R
   pQ = 0
   for i in range(n):
      for j in range(n):
         mat[i,j] = matrix[i,j] / R[i]
         if(i!=j):
            if(matrix[i,j]>0):
               pQ += (N[i,j] + alpha[i,j] -1) * np.log(mat[i,j]) - mat[i,j] * (beta[i] + R[i])
   return pQ

def gammaFunction(x, alpha, beta):
   if(x<0 or alpha<=0 or beta<=0):
      print "gamma function encountered a negative/zero value"
      print x, alpha, beta
      quit()
   t1 = beta**alpha
   if(x!=0):
      t2 = x**(alpha-1)
   else:
      t2=0
   t3 = math.exp(-1 * beta * x)
   gam = math.factorial(int(alpha-1))
   ret = t1 * t2 * t3 / gam
   return ret

def makeNewQ(Q, alpha, beta):
   n = Q.shape[0]
   q = np.zeros((n,n))
   for i in range(n):
      for j in range(n):
         q[i,j] = gammaFunction(Q[i,j], alpha[i,j], beta[i])
   return q

def nextState(probs,sort):
#   print probs, sort
#   print probs.dtype
   key = np.zeros(probs.shape[0])
   f=0
   for i in range(key.shape[0]):
      while(key[i]==0):
         f+=1
#         print sort[i], probs[f-1]
         if(sort[i] == probs[f-1]):
            key[i] = f
            f=0
            
   randomNumber = random.random()
   n = sort.shape[0]
   for i in range(key.shape[0]):
      if(sort[n-i-1]>=randomNumber):
         return key[n-i-1]-1
      else:
         randomNumber -= sort[i]
   print sort
   print randomNumber
   print "ERROR : nextState Failed: Quitting"
   quit()

def takeStep(matrix, x, iterationsPerStep):#this should be coupled with an array which starts from each state

   Probs = expm(matrix)
   while(iterationsPerStep>0):
      iterationsPerStep-=1
      normProbColumn = np.zeros(Probs.shape[0])
      normProbColumn = Probs[:,x] / np.sum(Probs[:,x]) #normalized probability, doesn't take into account negative elements o.0
      sort = np.sort(normProbColumn)
      x = int(nextState(normProbColumn, sort))
   return x
def makeNewNMatrix(matrix):#takes in generated matrix which has dimension nxt
#where n = number of possible states
#and t is number of time steps per iteration
   n = matrix.shape[0]
   t = matrix.shape[1]
   N = np.zeros((n,n))
   for i in range(n):
      for j in range(t):
         if(j!=0):
            N[int(matrix[i,j-1]),int(matrix[i,j])] +=1
   return N
