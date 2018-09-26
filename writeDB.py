#!/usr/bin/python
import sys
import numpy as np
import matrixFunctions2d
from scipy.linalg import expm, logm

matrix =matrixFunctions2d.read2dMatrix(sys.argv[1])

Norm = matrixFunctions2d.normalize2dMatrix(matrix, 1)
logd = logm(Norm)


#mat = expm(matrix)
#matrixFunctions2d.printDetailedBalanceftxt(mat, "quickout.txt")
matrixFunctions2d.writeDetailedBalanceftxt(logd)
#matrixFunctions2d.printDetailedBalanceftxt(matrix, "quickout.txt")

