#!/usr/bin/python
import numpy as np
from scipy.linalg import expm, logm
import random
import sys
import matrixFunctions2d

#NMATRIX = matrixFunctions2d.read2dMatrix(sys.argv[1])
#distribution = matrixFunctions2d.normalize2dMatrix(NMATRIX,1)#normalize along rows
#n = distribution.shape[0]#24 #must equal shape of matrix we're importing

def stepGenerator(x, Q):
   prob = expm(Q)
   probs = np.zeros(prob.shape[0])
   probs = prob[:,x] / np.sum(prob[:,x]) #normalized along correct row (ignore negatives)
#this is where you can flatten probabilities if desired
   sort = np.sort(probs)
   return int(nextState(probs, sort))
   



def nextState(probs,sort):
   key = np.zeros(probs.shape[0])
   f=0
   for i in range(key.shape[0]):
      while(key[i]==0):
         f+=1
         if(sort[i] == probs[f-1]):
            key[i] = f
            f=0

   randomNumber = random.random()
   n = sort.shape[0]
   for i in range(key.shape[0]):
      if(sort[n-i-1]>=randomNumber):
         return key[n-i-1]-1
      else:
         randomNumber -= sort[n-1-i]
   print sort
   print randomNumber
   print "ERROR : nextState Failed: Quitting"
   quit()



def stepSimple(theta, Q=0):#either go up or down one.
   u = random.random()
   if(u>0.5):
      return theta + 1
   else:
      return theta - 1

def transitionProbSimple(xP, x, distribution, n):
   if (xP>n-1 or xP<0):
      return 0 #can't go outside of boundaries
   return distribution[x,xP] / distribution[x,x] #transition from x to xP divided by time spent in X


def metropolisHastings(niters, repeats, Nstate, distribution, deltaT, transitionProbs=transitionProbSimple, prior=stepSimple, Q=0):
   accept = 0.0
   totalCount = 0
   samples = np.zeros(niters*Nstate*repeats)#states * niters * repeats
   states = np.arange(Nstate)#each possible starting point
   for state in states:
      for r in range(repeats):
         theta = state
         thetaP = state
         for i in range(niters):
            for s in range(deltaT):
               thetaP = prior(thetaP, Q)
            p = random.random()/100 #these transitions are unlikely, so we'll make them more likely

            if(p<(transitionProbs(thetaP, theta, distribution, Nstate))):
               theta = thetaP
               accept +=1
            samples[totalCount] = theta
            totalCount+=1 #total count
   return samples, accept, totalCount


def countSamples(samples, Nstate):
#print out counting statistics
   counts = np.zeros(Nstate)
   for i in range(samples.shape[0]):
#      print samples[i],
      counts[int(samples[i])] +=1

   return counts

def printCounts(fname, totalCount, accept, Nstate, counts, xval):
   print "read file: ", fname
   print "total Count: ", totalCount
   print "percent accepted = ", accept/totalCount
   x = xval/2 * -1.0
   for i in range(Nstate):
      x += 1.0/(Nstate/xval)
      print x, counts[i]

def samplesToN(samples, Nstate):
   matrix = np.zeros((Nstate,Nstate))
   f=0
   #make Nij matrix
   for i in range(samples.shape[0]):
      if(i!=0):
         matrix[int(samples[i-1]),int(samples[i])] += 1
   for i in range(Nstate):
      matrix[i,i] += 1
   return matrix
def nToDB(matrix,Nstate,xval):
   x = xval/2 * -1.0
   print "Detailed Balance: "
   for i in range(Nstate):
      x+=1.0/(Nstate/xval)
      kbT = 0.00198 * 300
      f += -1.0 * kbT * np.log(abs(matrix[i+1,i])/abs(matrix[i,i+1]))
      print x, f

