#!/bin/bash
  for i in `ls EM_db_N*`; do python /home/cgoolsby/Documents/gitFolders/matrixFunctions/calcTransitionEnergy.py $i; done > EM_stats.comp
  for i in `ls detailed*`; do python /home/cgoolsby/Documents/gitFolders/matrixFunctions/calcTransitionEnergy.py $i; done > DB_stats.comp
  for i in `ls diagonal_db*`; do python /home/cgoolsby/Documents/gitFolders/matrixFunctions/calcTransitionEnergy.py $i; done > diagonal_stats.comp
  for i in `ls weighted_db*`; do python /home/cgoolsby/Documents/gitFolders/matrixFunctions/calcTransitionEnergy.py $i; done > weighted_stats.comp
  for i in `ls Nai*`; do python /home/cgoolsby/Documents/gitFolders/matrixFunctions/calcTransitionEnergy.py $i; done > Naive_stats.comp

