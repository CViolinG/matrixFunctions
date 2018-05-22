#!/usr/bin/python

import sys
import numpy as np
from scipy.linalg import expm, logm
import matrixFunctions2d



###########
#This file takes up to 3 inputs, first, the file to open, 2nd the file to write to, and third a '1' c$
###########

if(len(sys.argv)<3):
   print "This file takes up to 3 inputs, first, the file to open, 2nd the file to write to and third"
   quit()
k=0
if(len(sys.argv)>3):
   if(sys.argv[3]=='1'):
      k=1



N = matrixFunctions2d.read2dMatrix(sys.argv[1])
print "Opened %s"% sys.argv[1]

#matrixFunctions2d.print2dMatrix(N)
#print


print "Output will be written to %s"%sys.argv[2]


if(k==0):
   print "Currently Configured to sum along the COLUMN"
else:
   print "Currently Configured to sum along the ROW"


Norm = matrixFunctions2d.normalize2dMatrix(N, k)
#matrixFunctions2d.print2dMatrix(Norm)
n = N.shape[0]
#print
#now we solve n reduced optimization problems

Sort = np.copy(Norm)
Sort = Sort * -1#opposite of ascending sort is a
for i in range(n):#descending sort
   if(k==1):
      Sort[i,:].sort()
   else:
      Sort[:,i].sort()

Sort = Sort * -1 #restore to original negativity
#matrixFunctions2d.print2dMatrix(Sort)

Unsort = np.zeros((n,n))

#creating an NxN matrix which will allow the original matrix to be unsorted at the end
#print Sort[0,:]
#print Norm[0,:]
if(k==1):
   for i in range(n):
      for j in range(n):
         f=0
         while(Unsort[i,j]==0):
            if((Sort[i,f]==Norm[i,j])):
               Unsort[i,j] = f+1
            f+=1
else:
   for i in range(n):
      for j in range(n):
         f=0
         while(Unsort[j,i]==0):
            if((Sort[f,i]==Norm[j,i])):
               Unsort[j,i] = f+1
            f+=1





   
def findMValue(array):
   m=1
   n = len(array)
   S=0
#   print array
   for i in range(n):
      if(i==0):
         S=0
      else:
         S+= float(i*(array[i-1] - array[i]))
#         print "i: ", i, "S: ", S
#         quit()
         if(S>=1):
            m = i
            return m, S
   return m, 0

m = np.zeros(n)
S = np.zeros(n)
for i in range(n):
   if(k==0):
      m[i], S[i] = findMValue(Sort[:,i])
   else:
      m[i], S[i] = findMValue(Sort[i,:])
print S
print m


#calc lambdas
#l = np.zeros(n)
#for i in range(n):
#   m_ = int(m[i])
#   print m_
#   for j in range(m_):
#      if(k==1):
#         l[i] += 1.0/(1+m_) * (1.0 - Sort[i,j])
#         print "l is a combo of : ", 1.0/(1+m_), (1.0 - Sort[i,j]), "giving: ", 1.0/(1+m_) * (1.0 - Sort[i,j])
#         print "l : ", l
#      else:
#         l[j] += 1.0/(1+m_) * (1.0 - Sort[j,i])
#         print "l is a combo of : ", 1.0/(1+m_), (1.0 - Sort[j,i]), "giving: ", 1.0/(1+m_) * (1.0 - Sort[j,i])
#         print "l : ", l
#   print
#   print

l = np.zeros(n)
for i in range(n):
   if not(m[i] == 1):
      if(k==1):
         l[i] = (1.0-S[i])/m[i] - Sort[i,m[i]]
      if(k==0):
         l[i] = (1.0-S[i])/m[i] - Sort[m[i],i]

for i in range(n):
   if(k==1):
      for j in range(n):
         if(j>m[i]):
            Sort[i,j] = 0
         elif(j==0):
            Sort[i,j] = Sort[i,j] + l[i]
         else:
            Sort[i,j] = Sort[i,j] + l[i]
   else:
      for j in range(n):
         if(j>m[i]):
            Sort[j,i] = 0
         elif(j==0):
            Sort[j,i] = Sort[j,i] + l[i]
         else:
            Sort[j,i] = Sort[j,i] + l[i]



#matrixFunctions2d.print2dMatrix(Sort)

#use Unsort Matrix to get final output


final = np.zeros((n,n))
if(k==1):
   for i in range(n):
      for j in range(n):
         final[i,j] = Sort[i,Unsort[i,j]-1]
else:
   for i in range(n):
      for j in range(n):
         final[j,i] = Sort[Unsort[j,i]-1,i]
#print
#print
#matrixFunctions2d.print2dMatrix(Unsort)
#print
#print
#matrixFunctions2d.print2dMatrix(final)
matrixFunctions2d.write2dMatrix(final, sys.argv[2])
