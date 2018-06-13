#!/usr/bin/python
import matrixFunctions2d
import EMHelper
import sys
from scipy.linalg import logm, expm

#quite simple, read in a matrix, normalize it, take the log and set it as Qo
input = matrixFunctions2d.read2dMatrix(sys.argv[1])
Norm = matrixFunctions2d.normalize2dMatrix(input, 0)#currently works along rows, as does this whole algorithm


logd = logm(Norm)
#logd = logm(input)

diag = matrixFunctions2d.diagonalAdjustment2d(logd)
#matrixFunctions2d.print2dMatrix(diag)
#print
#print
epsilon = 0.000000000001
i=0
exit = 0
while(exit==0):
   diag, dist, exit = EMHelper.nextTimeStep(diag, epsilon)
   i+=1
   print i, dist
#   print
#   matrixFunctions2d.print2dMatrix(diag)
#   print
#   print


#matrixFunctions2d.print2dMatrix(diag)
#Norm = matrixFunctions2d.normalize2dMatrix(diag,1)
#matrixFunctions2d.printDetailedBalanceftxt(Norm, "db.txt")
matrixFunctions2d.write2dMatrix(diag, "EM_Matrix_%s.dat"%sys.argv[1])
matrixFunctions2d.printDetailedBalanceftxt(diag, "EM_db_%s.dat"%sys.argv[1])
