#!/bin/bash
# This process require at least 8000M of RAM memory per CPU
# require openmpi/3.1.2
# require mpi4py/3.0.0

# 1st parametter: Number of paralel task to compute, (2) is required if the user need to analyse BAF and LLR jointly
# 2nd parametter: Interval of sample to extract from a known sample list.
# 3rd parametter: Based directory path where transposed data are located 
# 4th parametter: Output directory path to save reduced final report input for CNV calling

# This process is highly parallelizable.

script=/path_to_the_folder/UKBB_DATA_GENERATOR/generateFinalReportFromTransposeData.py
tasks=$1
intervallToAnalyse=$2
baserawDir=$3
finalRepDir=$4

mpirun -np $tasks python3 $script $intervallToAnalyse $baserawDir $finalRepDir

