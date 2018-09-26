#!/usr/bin/python

import matrixFunctions2d
import sys
import numpy as np
matrix = matrixFunctions2d.read2dMatrix(sys.argv[1])
#matrix = matrixFunctions2d.normalize2dMatrix(matrix,1)
n = matrix.shape[0]
kb = 0.001987191683
t = 298 
kbt = kb * t
j=-2
FE = np.zeros(n)
print "\"Naive : %s\""%sys.argv[1]
sumd = 0
for i in range(n-1):
   j+=4.0/n
   sumd = np.sum(matrix[i,:])#sum of a row.
   #sumd = np.sum(matrix[:,i])#sum of a column.

   FE[i] = -kbt * np.log(sumd)
   print j,  FE[i]


