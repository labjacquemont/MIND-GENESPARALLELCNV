#!/bin/bash
# This process require at least 8000M of RAM memory per CPU
# require openmpi/3.1.2
# require mpi4py/3.0.0

# The parametter chunk is the batch size the user want to create. For example, for a cohort of 500000 individuals if the
# user indicate chuck as 50000, the scripts will split all individuals but it will organise them in 10 batches where each have ~50k
# samples.
# This process is highly parallelizable.

script=/path_to_the_folder/UKBB_DATA_GENERATOR/generateFinalReportFromTransposeData.py
tasks=$1
chunk=$2
mpirun -np $tasks python3 $script $chunk
