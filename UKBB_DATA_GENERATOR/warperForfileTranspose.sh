#!/bin/bash

# openmpi/3.1.2
# mpi4py/3.0.0
# Above libraries are required 

# We indicated the number of process as 2 (np 2), this means we will run 2 parallel jobs where
# BAF and LLR data split and transpose will be proceed.
# The parametter maxMem indicate the maximum dedicated RAM memory for the split chuck matrix file
# The bigger the reserved memory, the higher dimension will be the transposed chuncked matrix and
# therefore more chance for the process to end up with a OOM (Out of memory) error. it's recommended
# to request low computational memory with the consequence of generation high number of temporary files.
# A the end, the temporary files will all need to be paste side by side knowing that their are already
# transposed.

script=/path_to_UKBB_DATA_GENERATOR/formatUKBBdataToFinalReport.py
task=$1
chrom=$2
maxMem=$3
pathRawData=$4
options=$5

mpiexec -np $task python3 $script $chrom $maxMem $pathRawData $options

