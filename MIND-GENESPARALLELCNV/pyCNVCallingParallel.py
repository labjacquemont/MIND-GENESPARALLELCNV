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
 
Understanding the parametters
the parametters are capture by the sys.argv module

@1st parametter: Raw signal files combined in a list with their paths and the files.
  the list is provided as argument 1
@2nd parameter: the number of parallel task provided by the user
@3rd parametter: is the output folder location for the pennCNV cnv calls results
@4th parametter: is the output	folder location	for the	quantiSNP cnv calls results  
@5th parameter: is a specific interval fraction of the dataset	that the user want to 
  call CNV for,	if one need to call cnv	on the whole list then use the followin	parametter
  0-all
@6th is the batch id prefix for the cohort subset, if one haven't create subset for the
  projet dataset, then use 0 as prefix, therefor the results will be expected on folder
  named BATCH_00
@7th parametter: The quantisnp executor script provided on this pipeline bundle
@8th parametter: The pennCNV executor script provided on this pipeline bundle
@9th parametter: The sex file data localisation link, required by pennCNV and quantiSNP
@10th parametter: The pfb file localisation link, required by pennCNV and quantiSNP
@11th parametter: The gcmodel file file localisation link, required only for pennCNV
@12th parametter: The hmm file file localisation link, required only for pennCNV
@13th parametter: Is a boolean parametter to switch on/off the pennCNV calling process
                  the values are True or False
@14th parametter: Is a boolean parametter to switch on/off the quantiSNP calling process
       	       	  the values are True or False
@15th parametter: Directory path to the pennCNV installation
@16th parametter: Directory path to the quantiSNP installation
@17th parametter: The levels data file file localisation link, required only for quantiSNP
@17th parametter: PennCNV taskk to be executed, the below task are only active when pennCNV
                  execution is set to True: 
                  detect  (to run the cnv detection by pennCNV)
                  hmm     (to compute the training of the hmm file for a specific cohort)
                  quality (to compute only the summary quality of the samples)
"""
import sys,os
from mpi4py import MPI
import subprocess
import getpass

def parallelCNVcallPipeline():
    user=getpass.getuser()
    tabFactor1=int(sys.argv[5].split("-")[0])
    try:
        tabFactor2=int(sys.argv[5].split("-")[1])
    except:
        tabFactor2="all"
    
    SamplesFile=open(sys.argv[1],'r')
    tabSamples=[]
    for samples in SamplesFile:
        samples=samples.rstrip("\n")
        samples=samples.replace("lyon",user)
        tabSamples.append(samples)
    if tabFactor2=="all":
        tabFactor2=len(tabSamples)

    nbProcess=int(sys.argv[2])
    tabSamplesTemp=tabSamples[tabFactor1:tabFactor2]
    tabSamples=tabSamplesTemp
    batch=sys.argv[6]
    user=getpass.getuser()
    output=sys.argv[3]
    os.system("mkdir -p "+output+"/BATCH_0"+batch)
    outputPenn=sys.argv[4]
    os.system("mkdir -p "+outputPenn+"/BATCH_0"+batch)
    os.system("mkdir -p "+outputPenn+"/BATCH_0"+batch+"/LOG_DATA")
    os.system("mkdir -p "+outputPenn+"/BATCH_0"+batch+"/CNV_DATA")
    i=0
    while i<(len(tabSamples)):
        if i+nbProcess>len(tabSamples):
            paralleleExec(tabSamples[i:len(tabSamples)])
        else:
            paralleleExec(tabSamples[i:i+nbProcess])
        i=i+nbProcess
            
def paralleleExec(samplesTab):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()    
    try:
        execScript(samplesTab[rank])
    except:
        pass

def execScript(sample):
    hmmFile=sys.argv[12]
    batch=sys.argv[6]
    sampleID=os.path.basename(sample).split(".")[0]
    QuantiSNPscript=sys.argv[7]
    PennCNVscript=sys.argv[8]
    sex=sys.argv[9]
    pfb=sys.argv[10]
    gcmodel=sys.argv[11]
    outputQuantiSNP=sys.argv[3]+"/BATCH_0"+batch
    outputPennCNV=sys.argv[4]+"/BATCH_0"+batch
    pathToPennCNV=sys.argv[15]
    pathToQuantiSNP=sys.argv[16]
    quantiSNPlevelsData=sys.argv[17]
    pennTask=sys.argv[18]
    if sys.argv[14]=="True":
        if (os.path.isfile(outputQuantiSNP+"/"+sampleID+".outdir/"+sampleID+".cnv")==False or os.path.isfile(outputQuantiSNP+"/"+sampleID+".outdir/"+sampleID+".qc")==False):
            print("Computing quantiSNP CNV calls for sample: \n"+sample)
            subprocess.call([QuantiSNPscript,sample,outputQuantiSNP,sex,pathToQuantiSNP,quantiSNPlevelsData])

    if sys.argv[13]=="True":
        if os.path.isfile(outputPennCNV+"/CNV_DATA/autosome_"+sampleID+".rawcnv")==False or os.path.isfile(outputPennCNV+"/CNV_DATA/gonosome_X_"+sampleID+".rawcnv")==False or os.path.isfile(outputPennCNV+"/CNV_DATA/autosome_"+sampleID+".log")==False or os.path.isfile(outputPennCNV+"/CNV_DATA/gonosome_X_"+sampleID+".log")==False:
            if pennTask=="detect":
                print("Computing PennSNV CNV calls for sample: \n"+sample)
            elif pennTask=="hmm":
                print("Computing PennSNV HMM training for all sample\n")
            elif pennTask=="quality":
                print("Computing PennSNV quality summary for sample: \n"+sample)
            else:
                print("Wrong PennCNV execution input provided")
            subprocess.call([PennCNVscript,pathToPennCNV,sample,outputPennCNV,pfb,sex,gcmodel,hmmFile,pennTask])


parallelCNVcallPipeline()
