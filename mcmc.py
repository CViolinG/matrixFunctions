#!/usr/bin/python
import matrixFunctions2d
import MCMCHelper
import numpy as np
from scipy.linalg import expm, logm
import sys
import random
start = matrixFunctions2d.read2dMatrix(sys.argv[1])
startN = matrixFunctions2d.normalize2dMatrix(start, 1) #Normalize along row

startL = logm(startN)
startW = matrixFunctions2d.weightedAdjustment2d(startL, 1)# along row
#matrixFunctions2d.print2dMatrix((startW))
#quit()
t=0
k=1000
r=0
#dA = 0
#dB = 0
n = startL.shape[0]
alpha = np.zeros((n,n))
beta = np.zeros(n)
alpha[:,:] = 1
beta[:] = 1
alpha0 = np.copy(alpha)
beta0 = np.copy(beta)
Q = MCMCHelper.makeNewQ(alpha, alpha, beta, alpha)#generates a random Q
#matrixFunctions2d.print2dMatrix(Q)
while(t<10000):
   q = np.copy(Q)
   states = np.zeros(3*n)
   for i in range(n):
      states[3*i] = i
      states[3*i+1] = i
      states[3*i+2] = i

   #sample
   markovChain = np.zeros((3*n,k))
   deltaT = 20 
   for state in states:
      markovChain[state,0] = state
      p=0
      while(p<k-1):
         markovChain[state, p+1] = MCMCHelper.takeStep(q, int(markovChain[state,p]), deltaT)
#         print markovChain[state,p], markovChain[state,p+1]
         rando = random.random()
         s1 = int(markovChain[state,p])
         s2 = int(markovChain[state,p+1])
         compare = -1.0 * startW[s2,s1] / startW[s1,s1]
#         if(abs(s1-s2)==1):
#            print s1, s2, rando, compare, p
         if(rando < compare or s1==s2):
            p+=1 
            if(p%100==0):
               print p, state
#               print markovChain[state, :p]
   t+=1
#   print r, printstring, pQ
   print t

   startM = MCMCHelper.makeNewNMatrix(markovChain)
   startN = matrixFunctions2d.normalize2dMatrix(startM, 1)
   Q = MCMCHelper.makeNewQ(startN, alpha0, beta0, start)#currently start doesn't matter


   matrixFunctions2d.printDetailedBalanceftxt(q, "worked.txt")





