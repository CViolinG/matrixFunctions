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
#matrixFunctions2d.print2dMatrix(expm(startN))
#quit()
t=0
k=100
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
pQ = MCMCHelper.posteriorQ(startN, startN, alpha, beta)
Q = np.copy(startN)
while(t<1000):
   q = np.copy(Q)
   accept=0
   states = np.arange(n)
#   matrixFunctions2d.print2dMatrix(start)
#   quit()
#   startL = logm(start)
#   startW = matrixFunctions2d.weightedAdjustment2d(startL, 1)


   while(accept==0):
      markovChain = np.zeros((n,k))
      for i in range(n):
         markovChain[i,0] = states[i]
         p=0
         while(p<k-1):
            markovChain[i,p+1] = MCMCHelper.takeStep(q, int(markovChain[i,p]), 2)
            p+=1

      startM = MCMCHelper.makeNewNMatrix(markovChain) #returns a unNormalized Matrix
      startN = matrixFunctions2d.normalize2dMatrix(startM)
      Q = MCMCHelper.makeNewQ(startN, alpha0, beta0)
      pQtest = MCMCHelper.posteriorQ(Q, startN, alpha0, beta0)
      if(pQtest>pQ):
         alpha = alpha0
         beta = beta0
         accept = 1
         r=0
         print "Accept ", r, pQtest, pQ
         pQ = pQtest
      else:
         for i in range(n):
            beta0[i] = abs(beta0[i] + random.random()-0.5)
            for j in range(n):
               alpha0[i,j] = abs(alpha0[i,j] + random.random()-0.5)
         accept = 0
         r+=1 #convergenace criteria
         print "Reject ", r, pQtest, pQ
         if(r>5):#converged
            print t, "Converged"
            matrixFunctions2d.print2dMatrix(q)
            matrixFunctions2d.printDetailedBalanceftxt(q, "converged.txt")
            quit()


   printstring = "data/cycle." + str(t) + ".txt"
   matrixFunctions2d.write2dMatrix(q, printstring)

   t+=1
   print r, printstring, pQ

   matrixFunctions2d.printDetailedBalanceftxt(q, "worked.txt")





