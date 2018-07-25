#!/usr/bin/python
import sys
import numpy as np
file = open(sys.argv[1])
left = mid = right = 0
linecount = 0
for line in file.xreadlines():
   ar = line.split()
   linecount+=1
   if(linecount<3):
      continue 
   if(float(ar[0]) == -1.0):
      left = float(ar[1])
   if(float(ar[0]) == 1.0):
      right = float(ar[1])
   if(abs(float(ar[0]))<0.00000000000001):
      mid = float(ar[1])
print sys.argv[1], " : ", left, mid, right, right-left, mid-left 
