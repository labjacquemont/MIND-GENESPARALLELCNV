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
are respected.
 
Understanding the parametters
the parametters are capture by the sys.argv module

@1st parametter: The chromosome to execute
@2nd parameter:  The per batch size 
@3nd parameter:  Complete path to the UKBB raw data directory
@4nd parameter:  Data task or tasks to execute in array style. Example: BAF:LLR:CR
                 B allele frequency BIG matrix will be fragmented, transposed and
                 merged, next, LLR (Log R Ratio) and CR (GC score). the GC score transposed
                 data is used to compute the call rate by a different script.
"""

import codecs,sys,math
import sys,os
from mpi4py import MPI
import subprocess,time
import numpy as np
import pandas as pd
import psutil
import glob
from natsort import natsorted

def reformatRAWdataBAF():
    chrom=sys.argv[1]
    os.system("mkdir -p "+sys.argv[3]+"/UKB_genotype_baf")
    BAF=sys.argv[3]+"/UKB_genotype_baf/ukb_baf_chr"+chrom+"_v2.txt"
    BAFroot=sys.argv[3]+"/UKB_genotype_baf"
    os.system("mkdir -p "+BAFroot+"/fragmentedBAF_chr"+chrom)
    BAFpdDF=pd.DataFrame(np.array([[],[]]))
    temporaryArray=[]
    partFileInd=0
    currentDFsize=0
    inTime=time.time()
    perTaskMemSize=int(sys.argv[2])
    for line in open(BAF,'r'):
        line=line.rstrip("\n").split(" ")
        #line=convertToNumeric(line)
        temporaryArray.append(line)
        if len(temporaryArray)==200:
            print("(BAF):", int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize<5,int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize)
            temporaryPdDF=pd.DataFrame(np.array(temporaryArray).transpose())
            print("(BAF): Data transpose time= ",round((time.time()-inTime)/60,2),"mn")
            currentDFsize+=temporaryPdDF.memory_usage(deep=True).sum()/((1024)*(1024)*(1024))
            BAFpdDF=pd.concat([BAFpdDF,temporaryPdDF],axis=1,ignore_index=True,sort=False)
            print("(BAF): Dataframe concatenation time= ",round((time.time()-inTime)/60,2),"mn")
            temporaryArray=[]
            print("(BAF): Dataframe current part size: ",round(currentDFsize,2)," Gb")
        
        if currentDFsize/perTaskMemSize>=0.2:
            BAFfout=open(BAFroot+"/fragmentedBAF_chr"+chrom+"/BAF.chr"+chrom+".part_"+str(partFileInd),'w')
            BAFfout.write(BAFpdDF.to_csv(sep="\t",index=False,header=False))
            BAFfout.close()
            currentDFsize=0
            outTime=(time.time()-inTime)/60
            print("(BAF): File generated time= ",round(outTime,2),"mn")
            #break
            BAFpdDF=pd.DataFrame(np.array([[],[]]))
            partFileInd+=1

    print("(BAF):", int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize<5,int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize)
    temporaryPdDF=pd.DataFrame(np.array(temporaryArray).transpose())
    print("(BAF): Data transpose time= ",round((time.time()-inTime)/60,2),"mn")
    currentDFsize+=temporaryPdDF.memory_usage(deep=True).sum()/((1024)*(1024)*(1024))
    BAFpdDF=pd.concat([BAFpdDF,temporaryPdDF],axis=1,ignore_index=True,sort=False)
    print("(BAF): Dataframe concatenation time= ",round((time.time()-inTime)/60,2),"mn")
    temporaryArray=[]
    print("(BAF): Dataframe current part size: ",round(currentDFsize,2)," Gb")

    BAFfout=open(BAFroot+"/fragmentedBAF_chr"+chrom+"/BAF.chr"+chrom+".part_"+str(partFileInd),'w')
    BAFfout.write(BAFpdDF.to_csv(sep="\t",index=False,header=False))
    BAFfout.close()
    BAFpdDF=pd.DataFrame(np.array([[],[]]))
    outTime=(time.time()-inTime)/60
    print("(BAF): File generated time= ",round(outTime,2),"mn")
    os.system("mkdir -p "+BAFroot+"/completeMergeBAF_chr"+chrom)

    arrayFile=glob.glob(BAFroot+"/fragmentedBAF_chr"+chrom+"/*.part*")
    arrayFile=natsorted(arrayFile,key=lambda y: y.lower())
    print("pasting all files together for BAF... nb files are:\t",len(arrayFile))
    os.system("paste -d\"\t\" "+(" ").join(arrayFile)+" > "+BAFroot+"/completeMergeBAF_chr"+chrom+"/completeMerge.chr"+chrom+".BAF.txt")
    

def reformatRAWdataLRR():
    chrom=sys.argv[1]
    os.system("mkdir -p "+sys.argv[3]+"/UKB_genotype_l2r")
    LRR=sys.argv[3]+"/UKB_genotype_l2r/ukb_l2r_chr"+chrom+"_v2.txt"
    LRRroot=sys.argv[3]+"/UKB_genotype_l2r"
    os.system("mkdir -p "+LRRroot+"/fragmentedLRR_chr"+chrom)
    LRRpdDF=pd.DataFrame(np.array([[],[]]))
    temporaryArray=[]
    partFileInd=0
    currentDFsize=0
    inTime=time.time()
    perTaskMemSize=int(sys.argv[2])
    for line in open(LRR,'r'):
        line=line.rstrip("\n").split(" ")
        #line=convertToNumeric(line)
        temporaryArray.append(line)
        if len(temporaryArray)==200:
            print("(LRR): ",int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize<5,int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize)
            temporaryPdDF=pd.DataFrame(np.array(temporaryArray).transpose())
            print("(LRR): Data transpose time= ",round((time.time()-inTime)/60,2),"mn")
            currentDFsize+=temporaryPdDF.memory_usage(deep=True).sum()/((1024)*(1024)*(1024))
            LRRpdDF=pd.concat([LRRpdDF,temporaryPdDF],axis=1,ignore_index=True,sort=False)
            print("(LRR): Dataframe concatenation time= ",round((time.time()-inTime)/60,2),"mn")
            temporaryArray=[]
            print("(LRR): Dataframe current part size: ",round(currentDFsize,2)," Gb")
        if currentDFsize/perTaskMemSize>=0.2:
            LRRfout=open(LRRroot+"/fragmentedLRR_chr"+chrom+"/LRR.chr"+chrom+".part_"+str(partFileInd),'w')
            LRRfout.write(LRRpdDF.to_csv(sep="\t",index=False,header=False))
            LRRfout.close()
            currentDFsize=0
            outTime=(time.time()-inTime)/60
            print("(LRR): File generated time= ",round(outTime,2),"mn")
            LRRpdDF=pd.DataFrame(np.array([[],[]]))
            partFileInd+=1

    print("(LRR): ",int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize<5,int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize)
    temporaryPdDF=pd.DataFrame(np.array(temporaryArray).transpose())
    print("(LRR): Data transpose time= ",round((time.time()-inTime)/60,2),"mn")
    currentDFsize+=temporaryPdDF.memory_usage(deep=True).sum()/((1024)*(1024)*(1024))
    LRRpdDF=pd.concat([LRRpdDF,temporaryPdDF],axis=1,ignore_index=True,sort=False)
    print("(LRR): Dataframe concatenation time= ",round((time.time()-inTime)/60,2),"mn")
    temporaryArray=[]
    print("(LRR): Dataframe current part size: ",round(currentDFsize,2)," Gb")

    LRRfout=open(LRRroot+"/fragmentedLRR_chr"+chrom+"/LRR.chr"+chrom+".part_"+str(partFileInd),'w')
    LRRfout.write(LRRpdDF.to_csv(sep="\t",index=False,header=False))
    LRRfout.close()
    LRRpdDF=pd.DataFrame(np.array([[],[]]))
    outTime=(time.time()-inTime)/60
    print("(LRR): File generated time= ",round(outTime,2),"mn")
    os.system("mkdir -p "+LRRroot+"/completeMergeLRR_chr"+chrom)

    arrayFile=glob.glob(LRRroot+"/fragmentedLRR_chr"+chrom+"/*.part*")
    arrayFile=natsorted(arrayFile,key=lambda y: y.lower())
    print("pasting all files together for LRR... nb files are:\t",len(arrayFile))
    os.system("paste -d\"\t\" "+(" ").join(arrayFile)+" > "+LRRroot+"/completeMergeLRR_chr"+chrom+"/completeMerge.chr"+chrom+".LRR.txt")


def reformatRAWdataCR():
    chrom=sys.argv[1]
    os.system("mkdir -p "+sys.argv[3]+"/GCSCORErawData")
    CR=sys.argv[3]+"/GCSCORErawData/ukb_con_chr"+chrom+"_v2.txt"
    CRroot=sys.argv[3]+"/GCSCORErawData"
    os.system("mkdir -p "+CRroot+"/fragmentedCR_chr"+chrom)
    CRpdDF=pd.DataFrame(np.array([[],[]]))
    temporaryArray=[]
    partFileInd=0
    currentDFsize=0
    inTime=time.time()
    perTaskMemSize=int(sys.argv[2])
    for line in open(CR,'r'):
        line=line.rstrip("\n").split(" ")
        
        temporaryArray.append(line)
        if len(temporaryArray)==200:
            print("(CR): ",int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize<5,int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize)
            temporaryPdDF=pd.DataFrame(np.array(temporaryArray).transpose())
            print("(CR): Data transpose time= ",round((time.time()-inTime)/60,2),"mn")
            currentDFsize+=temporaryPdDF.memory_usage(deep=True).sum()/((1024)*(1024)*(1024))
            CRpdDF=pd.concat([CRpdDF,temporaryPdDF],axis=1,ignore_index=True,sort=False)
            print("(CR): Dataframe concatenation time= ",round((time.time()-inTime)/60,2),"mn")
            temporaryArray=[]
            print("(CR): Dataframe current part size: ",round(currentDFsize,2)," Gb")
        if currentDFsize/perTaskMemSize>=0.2:
            CRfout=open(CRroot+"/fragmentedCR_chr"+chrom+"/CR.chr"+chrom+".part_"+str(partFileInd),'w')
            CRfout.write(CRpdDF.to_csv(sep="\t",index=False,header=False))
            CRfout.close()
            currentDFsize=0
            outTime=(time.time()-inTime)/60
            print("(CR): File generated time= ",round(outTime,2),"mn")
            CRpdDF=pd.DataFrame(np.array([[],[]]))
            partFileInd+=1

    print("(CR): ",int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize<5,int(dict(psutil.virtual_memory()._asdict())['total']/((1024)*(1024)*(1024)))%perTaskMemSize)
    temporaryPdDF=pd.DataFrame(np.array(temporaryArray).transpose())
    print("(CR): Data transpose time= ",round((time.time()-inTime)/60,2),"mn")
    currentDFsize+=temporaryPdDF.memory_usage(deep=True).sum()/((1024)*(1024)*(1024))
    CRpdDF=pd.concat([CRpdDF,temporaryPdDF],axis=1,ignore_index=True,sort=False)
    print("(CR): Dataframe concatenation time= ",round((time.time()-inTime)/60,2),"mn")
    temporaryArray=[]
    print("(CR): Dataframe current part size: ",round(currentDFsize,2)," Gb")

    CRfout=open(CRroot+"/fragmentedCR_chr"+chrom+"/CR.chr"+chrom+".part_"+str(partFileInd),'w')
    CRfout.write(CRpdDF.to_csv(sep="\t",index=False,header=False))
    CRfout.close()
    CRpdDF=pd.DataFrame(np.array([[],[]]))
    outTime=(time.time()-inTime)/60
    print("(CR): File generated time= ",round(outTime,2),"mn")
    os.system("mkdir -p "+CRroot+"/completeMergeCR_chr"+chrom)

    arrayFile=glob.glob(CRroot+"/fragmentedCR_chr"+chrom+"/*.part*")
    arrayFile=natsorted(arrayFile,key=lambda y: y.lower())
    print("pasting all files together for CR... nb files are:\t",len(arrayFile))
    os.system("paste -d\"\t\" "+(" ").join(arrayFile)+" > "+CRroot+"/completeMergeCR_chr"+chrom+"/completeMerge.chr"+chrom+".CR.txt")

def MPIexeDataFormat():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    tabtasks=sys.argv[4].split(":")
    if "BAF" in tabtasks:
        ranking=tabtasks.index("BAF")
        if rank==ranking:
            reformatRAWdataBAF()

    if "LLR" in tabtasks:
        ranking=tabtasks.index("LRR")
        if rank==ranking:
            reformatRAWdataLRR()

    if "CR" in tabtasks:
        ranking=tabtasks.index("CR")
        if rank==ranking:
            reformatRAWdataCR()


def convertToNumeric(array):
    for i in range(len(array)-1):
        try:
            temp=float(array[i])
            array[i]=temp
        except:
            array[i]=np.nan
    return array


MPIexeDataFormat()
