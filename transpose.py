#!/usr/bin/python

import numpy as np
import matrixFunctions2d
import sys
matrix = matrixFunctions2d.read2dMatrix(sys.argv[1])
out = np.transpose(matrix)

matrixFunctions2d.print2dMatrix(out)
