#!/usr/bin/python
import numpy as np
import matrixFunctions2d
import sys
from scipy import integrate


mat = matrixFunctions2d.read2dMatrix(sys.argv[1])
tau = int(sys.argv[2])


mat = matrixFunctions2d.normalize2dMatrix(mat, 1)
EV = np.linalg.eigvals(mat)
EV = np.real(EV)
EV=-1*np.sort(-1*EV)
print(EV)

kb = 0.0019872041
T = 298
kbT = kb * T
#print kbT
beta = 1/kbT
#print beta
def pot(x,k=10):
    return k/4.0 * (x**2 - 1)**2

def p(x, beta=beta):
    return np.exp(beta * pot(x))

def n(x, beta=beta):
    return np.exp(-1 * beta * pot(x))
#currently D(x) = 1 in all space
def D(x):
    kb = 0.0019872041
    T = 298
    kbT = kb * T
    return kbT

#Equation in Anjum Ansari paper titled "Mean First Passage Time solution of the Smoluchowski Equation: ...)
def inner(y):
    return integrate.quad(n, -4.0, y)[0]
def outer(x):
    return p(x) * inner(x)
MFPTpredicted = integrate.quad(outer,-1.0, 1.0)[0]
print MFPTpredicted
print "---"

def innerSum(lower, upper, delta=0.001):
    value=0
    i=lower
    while(i<=upper):
        value += n(i)* delta
        i+=delta
    return value
def outerSum(lower, upper, delta=0.001):
    value=0
    i=lower
    while(i<=upper):
        value += p(i) * innerSum(-4.0, i)* delta
        i+=delta
    return value
MFPTSum= outerSum(-1, 1)
print "SuM Prediction :", MFPTSum



MFPT = -tau/np.log(EV[1]) * 0.000001 #10^-6 is timestep
print MFPT

#for i in range(EV.shape[0]):
#    print i, EV[i]
