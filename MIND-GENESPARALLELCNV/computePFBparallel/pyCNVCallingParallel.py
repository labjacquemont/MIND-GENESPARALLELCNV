#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 00:30:13 2019
@author: Martineau jean-Louis
This CNV call pipeline is dedicated to call detect CNV through both 
QuantiSNP and PennCNV algorithm. More algorithm cnv calls will be added
such as Ipattern, bcftools, DNAcopy and fastSeg. this version is release
on October 4th 2019 and will be updated very often. Any code optimization
and CNV calling algorith suggestion are welcome.

As part of the JacquemontLab, I provide sharing permission and rigth for 
collaborators and lab group members to share algorithm and code contents
of the pipeline as long as the digital and intellectual contents policies
are applied.
"""
import sys,os
from mpi4py import MPI
import subprocess
import gzip
import getpass


def pfbGENERATOR():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 22:
        chrom="X"
    elif rank == 23:
        chrom="Y"
    else:
        chrom=str(rank+1)
    splitSampleList=sys.argv[1]
    splitMarkerList=sys.argv[2]
    outputResults=sys.argv[3]
    script="./PFBexecutor.sh"
    inputSample=splitSampleList+"/samplesForPFB.chr"+chrom+".txt"
    inputMarker=splitMarkerList+"/markerlist.chr"+chrom+".list"
    outputPFBfile=outputResults+"/pfbResults.chr"+chrom+".pfb"
    
    subprocess.call([script,inputSample,outputPFBfile,inputMarker])

pfbGENERATOR()
