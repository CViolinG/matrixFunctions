#!/usr/bin/python
import numpy as np
import scipy as sp
from scipy.linalg import expm, logm
import os.path

def normalize2dMatrix(matrix, k=0): #if k = 1, normalize along rows instead of columns
   n = matrix.shape[0]
   Norm = np.copy(matrix)
   sum = np.zeros(n)
   for i in range(n):
      for j in range(n):
         if(k==0):
            sum[i] += Norm[j,i]#Columns
         else:
            sum[i] += Norm[i,j] #rows
#divide by sum
   for i in range(n):
      for j in range(n):
         if(k==0):
            Norm[i,j] = Norm[i,j] / sum[i]
         else:
            Norm[j,i] = Norm[j,i] / sum[i]


   return Norm



def read2dMatrix(fileName):
   i=0
   file = open(fileName)
   for line in file.xreadlines():
      if "," not in line:
         array = line.split()
      else:
         array = line.split(", ")
      if(i==0):
         matrix = np.zeros((len(array),len(array)))
      matrix[i] = array
      i+=1
   if(matrix.shape[0]!=matrix.shape[1]):
      print "Error: Your Matrix is not square, Exiting!"
      quit()
   return matrix



def diagonalAdjustment2d(matrix, k=0):

#The diagonal adjustment takes any offdiagonal negative numbers and sets them to zero
#then the diagonal elements are set to the negative sum of the non-diagonal elements
#i.e. qii = -SUM{qij for j!=i}

#I think this is the row? Look at the bottom of page 13(of Inamura) to be certain.
   n = matrix.shape[0]
   for i in range(n):
      for j in range(n):
         if(i!=j and matrix[i,j]<0):
            matrix[i,j] = 0 #set negative off diagonals to zero
   sum = np.zeros(n)
   for i in range(n):
      matrix[i,i] = 0
      if(k==0):
         sum[i] = np.sum(matrix[:,i])
      else:
         sum[i] = np.sum(matrix[i,:])
      matrix[i,i] = -1 * sum[i]

   return matrix

def weightedAdjustment2d(matrix, k=0):
#The weighted adjustment takes any offdiagonal negative numbers and sets them to zero
#then the nonzero elements are adjusted based on the following
#qij = qij - |qij| * SUM{qij} / SUM{|qij|} 
#top of page 14
   n = matrix.shape[0]
   for i in range(n):
      for j in range(n):
         if(i!=j and matrix[i,j]<0):
            matrix[i,j] = 0#set negative offdiagonals to zero

   justSums = np.zeros(n)
   absSums = np.zeros(n)
   
   for i in range(n):
      for j in range(n):
         if(k==0):#column wise
            justSums[i] += matrix[i,j]
            absSums[i] += abs(matrix[i,j])
         if(k==1):#row wise
            justSums[i] += matrix[j,i]
            absSums[i] += abs(matrix[j,i])

   for i in range(n):
      justSums[i] = justSums[i] / absSums[i] #multiplication factor created

   for i in range(n):
      for j in range(n):
         if(k==0):
            matrix[i,j] = matrix[i,j] - abs(matrix[i,j]) * justSums[i]#columns
         if(k==1):
            matrix[i,j] = matrix[i,j] - abs(matrix[i,j]) * justSums[j]#rows
   return matrix
   


def print2dMatrix(matrix):
   n = matrix.shape[0]
   for i in range(n):
      for j in range(n):
         print "%8s " %matrix[i,j],
      print "\n",



def printDetailedBalanceftxt(matrix, fname, additionalComments=''):
   fname2 = fname
   n = matrix.shape[0]
   i=1
   kb = 0.00198
   t = 300
   kbt = kb * t
   while(os.path.isfile(fname2)):
      fname2 = fname + "." + str(i)
      i+=1
   ftxt = open(fname2, "w+")
   ftxt.write("\"%s\""%fname2)
   f = np.zeros(n)
   for i in range(n-1):
#      print i, matrix[i+1,i], matrix[i,i+1]
      if(matrix[i+1,i] == 0 or matrix[i,i+1]==0):
         f[i] = 0
      else:
         f[i] += f[i-1] + kbt * np.log(abs(matrix[i+1,i] / matrix[i,i+1]))
#      print f[i]
#   sumd = np.sum(f)
#   f = f/sumd
#   for i in range(n-1):
#      f[i] = f[i-1] - 0.6 * np.real(sp.log(f[i]))
   j=-2
   miin = np.min(f)
   ftxt.write("#Adjusted by min of: %s\n"%miin)
   ftxt.write("#%s\n"%additionalComments)
   if(miin<0):
      f += miin
   else:
      f -= miin
   for i in range(n-1):
      j+=4.0/n
      ftxt.write("%23s %23s\n"%(j,f[i]))
   ftxt.close()
   return fname2


def write2dMatrix(matrix, fname):
   fname2 = fname
   n = matrix.shape[0]
   i=1
   while(os.path.isfile(fname2)):
      fname2= fname+ "." + str(i)
      i+=1
   ftxt = open(fname2, "w+")
   for i in range(n):
      for j in range(n):
         ftxt.write("%23s "%matrix[i,j])
      ftxt.write("\n")
   ftxt.close()
   return fname2
