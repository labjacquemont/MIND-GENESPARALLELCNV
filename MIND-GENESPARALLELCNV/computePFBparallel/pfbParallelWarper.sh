#!/bin/bash

pyScript=~/CNV-calling/computePFBparallel/pyCNVCallingParallel.py
inputListSamples=/directory_path_to_the_fragmented_list_of_samples_per_chr/
inputListSNP=/directory_path_to_the_fragmented_list_of_SNP_per_chr/
outputResults=/directory_path_to_the_pfb_results_per_chr/

mpirun -np 24 python3 $pyScript $inputListSamples $inputListSNP $outputResults > pfbouput.log


