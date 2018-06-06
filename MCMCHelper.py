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
#   print R
   pQ = 0
   for i in range(n):
      for j in range(n):
         mat[i,j] = matrix[i,j] / R[i]
         if(i!=j):
            if(matrix[i,j]>0):
               pQ += (N[i,j] + alpha[i,j] -1) * np.log(mat[i,j]) - mat[i,j] * (beta[i] + R[i])
   return pQ

def gammaFunction(y, R, alpha, beta, x):
   beta += R###
   beta = 1/beta###
   alpha += y###
   x = random.random()# * random.randint(0, 10)###
   if(x<0 or alpha<=0 or beta<=0):
      print "gamma function encountered a negative/zero value"
      print x, alpha, y, beta , R
#      quit()
      return 0
   t1 = beta**alpha
   if(x!=0):
      t2 = x**(alpha-1)
   else:
      t2=0
   t3 = math.exp(-1 * beta * x)
#   print alpha, "-----"
   gam = 1 ##TECHNICALLY ALWAYS ONE RIGHT NOW ## math.factorial(int(alpha)-1)
   ret = t1 * t2 * t3 / gam
   return ret

def makeNewQ(mat, alpha, beta, start):
   n = mat.shape[0]
   q = np.zeros((n,n))
#   matrixFunctions2d.print2dMatrix(mat)
#   print
   Q = logm(mat)###
#   matrixFunctions2d.print2dMatrix(Q)
#   print
   R = np.zeros(n)###
   for i in range(n):###
      R[i] = np.sum(Q[i,:]) - Q[i,i]###
   for i in range(n):
      for j in range(n):
         if(i!=j):###
            q[i,j] = gammaFunction(Q[i,j], R[i], alpha[i,j], beta[i], start[i,j])###
   for i in range(n):###
      q[i,i] = 1.0 * np.sum(q[i,:])###
   return q

def flattenProbabilities(probs):
   #set np.max to 0.8 of sum of values
   #renormalize the vector
   #return the vector
#   probs[np.argmax(probs)] = 0.16 * (np.sum(probs) - probs[np.argmax(probs)])
   probs[np.argmax(probs)] = 4 * (np.sum(probs) - probs[np.argmax(probs)])
   probs /= np.sum(probs)
#   print probs
#   quit()
   return probs

def nextState(probs,sort):
#   quit()
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
#   print probs
#   print sort
   for i in range(key.shape[0]):
#      print sort[n-1-i], randomNumber, key[n-i-1]-1
      if(sort[n-i-1]>=randomNumber):
         return key[n-i-1]-1
      else:
         randomNumber -= sort[n-1-i]
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
      normProbColumn = flattenProbabilities(normProbColumn)
      sort = np.sort(normProbColumn)
      x = int(nextState(normProbColumn, sort))
   return x
def makeNewNMatrix(matrix):#takes in generated matrix which has dimension nxt
#where n = number of possible states
#and t is number of time steps per iteration
   n = 24#matrix.shape[0]
   t = matrix.shape[1]
   N = np.zeros((n,n))
   for i in range(n):
      for j in range(t):
         if(j!=0):
            N[int(matrix[i,j-1]),int(matrix[i,j])] +=1
   print "N"
   matrixFunctions2d.print2dMatrix(N)
   print
   return N

def checkReal(Q):
   n = Q.shape[0]
   for i in range(n-1):
      
      if(Q[i,i+1]==0 or Q[i+1,i]==0):
         return False
   return 1
