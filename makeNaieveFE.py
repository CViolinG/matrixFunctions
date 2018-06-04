#!/usr/bin/python

import matrixFunctions2d
import sys
import numpy as np
matrix = matrixFunctions2d.read2dMatrix(sys.argv[1])
n = matrix.shape[0]
j=-2
diag = np.zeros(n)
for i in range(n):
   j+=4.0/24
   diag[i] =  np.log(matrix[i,i])
   print j, diag[i]

#for i in range(11):
#   print diag[i] - diag[n-i-1]
