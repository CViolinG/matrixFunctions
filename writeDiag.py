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
diag = np.zeros(n)
print "\"Naive : %s\""%sys.argv[1]
sumd = 0
for i in range(n):
   sumd += matrix[i,i]
matrix = matrix/sumd
for i in range(n-1):
   j+=4.0/n
   diag[i] = -kbt * np.log(matrix[i,i])
   print j,  diag[i]


