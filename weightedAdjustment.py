#!/usr/bin/python

import sys
import numpy as np
import matrixFunctions2d
from scipy.linalg import logm, expm
###########
#This file takes up to 3 inputs, first, the file to open, 2nd the file to write to, and third a '1' can be passed in in order to sum along the rows instead of the columns
###########

if(len(sys.argv)<3):
   print "This file takes up to 3 inputs, first, the file to open, 2nd the file to write to and third a '1' can be passed in in order to sum along the rows instead of the columns"
   quit()
k=0
if(len(sys.argv)>3):
   if(sys.argv[3]=='1'):
      k=1



matrix = matrixFunctions2d.read2dMatrix(sys.argv[1])
print "Opened %s"% sys.argv[1]

out = open(sys.argv[2], "w+")
print "Output will be written to %s"%sys.argv[2]


if(k==0):
   print "Currently Configured to sum along the COLUMN"
else:
   print "Currently Configured to sum along the ROW"





n = matrix.shape[0]
print "Normalizing Input Matrix along ",
if(k==0):
   print "each column"
else:
   print "each row"

Norm = matrixFunctions2d.normalize2dMatrix(matrix, k)
#print Norm
log = logm(Norm)
adjusted = matrixFunctions2d.weightedAdjustment2d(log, k)

exp = expm(adjusted)

matrixFunctions2d.printDetailedBalanceftxt(exp, "f.txt")


#matrixFunctions2d.print2dMatrix(adjusted)
