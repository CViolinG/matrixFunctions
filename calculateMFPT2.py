#!/usr/bin/python
import numpy as np
import matrixFunctions2d
import sys
from scipy import integrate
from scipy.linalg import expm, logm

mat = matrixFunctions2d.read2dMatrix(sys.argv[1])
tau = int(sys.argv[2])

kb = 0.0019872041
T = 298
kbT = kb * T
#print kbT
beta = 1/kbT
#print beta
binWidth = 0.083333

#edit, first calculate DB statistics, then D(x), then double sum for an answer
#calculate DB
f = matrixFunctions2d.printDetailedBalanceftxt(mat, "temp")
#print f[11], f[35] Our -1, 1 are at 11/35 respectivelyi
lower=11
upper=35
adjustment=1 #the F index is off by one
lower=12
upper=36
adjustment=0
P=expm(0.000001*mat)
f = np.zeros(P.shape[0])
sumd=0
for i in range(P.shape[0]):
    sumd += P[i,i]
for i in range(P.shape[0]):
    f[i] = P[i,i]/sumd
for i in range(40):
#    f[i] = -1 * kbT * np.log(P[i,i]/binWidth) 
    f[i] += f[i-1] + kbT * np.log(abs(P[i+1,i] / P[i,i+1]))
#calculate the D(X) values
Q=np.copy(mat)
#Q = np.transpose(Q)
#Q=matrixFunctions2d.normalize2dMatrix(Q)
#for i in range(40):
#    print Q[i,i], Q[i+1,i], Q[i,i+1], np.sum(Q[i])
#quit()
#Q=matrixFunctions2d.normalize2dMatrix(Q,1)
#Q = matrixFunctions2d.normalize2dMatrix(mat)
#matrixFunctions2d.print2dMatrix(Q)
def innerHummer(upper, Q, f, beta=beta, binWidth=0.083333):
    inner=0
    for i in range(upper):
       inner+=np.exp(-1 * beta * f[i])
    return inner
def outerHummer(lower, upper, Q, f, a=adjustment, beta=beta, binWidth=0.08333):
    value = 0
    value2=0
    for i in range(lower, upper, 1):
        multiplier = innerHummer(i, Q, f)
        value2 += np.exp(f[i] * beta)/(np.sqrt(np.abs(Q[i+a,i+1+a] * Q[i+1+a,i+a]))) * multiplier
        #value2 += np.exp(f[i] * beta) * multiplier
        diff = value2-value
        value=value2
        print i, diff,value, np.sqrt(np.abs(Q[i+a,i+1+a] * Q[i+1+a,i+a]))
    return value
print outerHummer(lower,upper, Q, f)
quit()

mat = matrixFunctions2d.normalize2dMatrix(mat, 1)
EV = np.linalg.eigvals(mat)
EV = np.real(EV)
EV=-1*np.sort(-1*EV)
print(EV)

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
