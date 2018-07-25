#!/usr/bin/python
import numpy as np
import matrixFunctions2d
import sys

mat = matrixFunctions2d.read2dMatrix(sys.argv[1])

n = mat.shape[0]
for i in range(n):
   for j in range(n):
      if(mat[i,j]<0.00000000000001):
         mat[i,j] = 0
      else:
         mat[i,j] = 1


matrixFunctions2d.print2dMatrix(mat)
