#!/bin/bash

compilePFB="/home/j/jacquese/lyon/scratch/BIGFILE/SOFT/PennCNV-1.0.5/compile_pfb.pl"
snpPosFile=$3
listIDforPFB=$1
outputToPFB=$2

$compilePFB --listfile $listIDforPFB \
	--output $outputToPFB \
	--snpposfile $snpPosFile \
