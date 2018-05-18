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
            sum[i] += Norm[i,j]#Columns
         else:
            sum[i] += Norm[j,i] #rows
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
         sum[i] = np.sum(matrix[i,:])
      else:
         sum[i] = np.sum(matrix[:,i])
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
         print "%s" %matrix[i,j],
      print "\n",



def printDetailedBalanceftxt(matrix, fname):
   fname2 = fname
   n = matrix.shape[0]
   i=1
   while(os.path.isfile(fname2)):
      fname2 = fname + "." + str(i)
   ftxt = open(fname2, "w+")
   f = np.zeros(n)
   for i in range(n-1):
      f[i] = matrix[i+1,i] / matrix[i,i+1]
   sumd = np.sum(f)
   f = f/sumd
   f = -0.6 * np.real(sp.log(f))
   for i in range(n-1):
      ftxt.write("%s\n"%f[i])
   ftxt.close()
   return fname2
