#!/usr/bin/python

import sys
import numpy as np
from scipy.linalg import expm, logm
import scipy as sp
import matrixFunctions2d
k=0



matrix = matrixFunctions2d.read2dMatrix(sys.argv[1])






n = matrix.shape[0]

matrix = matrixFunctions2d.normalize2dMatrix(matrix, k)
matrix = logm(matrix)
matrix = np.real(matrix)
diag = matrixFunctions2d.diagonalAdjustment2d(matrix, k)
#print free energy to f.txt
matrixFunctions2d.write2dMatrix(diag, sys.argv[2])
matrixFunctions2d.writeDetailedBalanceftxt(diag)
