#!/usr/bin/python

import os
import sys

n = len(sys.argv) - 1
print "Filename:      Delta E (0)      Transition (2.5)"
for i in range(n):
  file = open(sys.argv[i+1])
  for line in file.xreadlines():
    ar = line.split()
    RL = ar[5]#delta E
    ML = ar[6]#transition state
    print "%10s   %10s   %10s"%(sys.argv[i+1], RL, ML)
  file.close()
  
  
