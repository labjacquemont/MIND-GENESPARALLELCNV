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


@1nd parameter:   The interval of an individual list to extract, for example, if the user
                  want to extract samples at position 20 to 40 then the 2nd param will be
                  "20:40"
@2nd parameter:   Complete path to the UKBB raw data directory
@3rd parametter:  Reduced Final report base directory
"""
from mpi4py import MPI
import sys,os,time

def createFinalReportFromTransposeData():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    intime=time.time()
    cpuProcessTime=intime
    IIDdata=open(sys.argv[2]+"/UKBB_fam_file/ukbb.fam",'r',encoding='utf-8')
    IIDarrayData=[]
    for sample in IIDdata:
        IIDarrayData.append(sample.rstrip("\n").split(" ")[1]+"_"+sample.rstrip("\n").split(" ")[5])
    SNParrayData=[]
    flaggedSNPdata=[]
    tabInstanceBAF=[]
    tabInstanceLRR=[]
    for chrom in range(1,24):
        if chrom==23:
            chrom="X"
        else:
            chrom=str(chrom)
        BAFbigMatrixData=open(sys.argv[2]+"/BAFrawData/completeMergeBAF_chr"+chrom+"/completeMerge.chr"+chrom+".BAF.txt", 'r',encoding='utf-8')
        tabInstanceBAF.append(BAFbigMatrixData)
        LRRbigMatrixData=open(sys.argv[2]+"/LRRrawData/completeMergeLRR_chr"+chrom+"/completeMerge.chr"+chrom+".LRR.txt", 'r', encoding='utf-8')
        tabInstanceLRR.append(LRRbigMatrixData)

        SNPdata=open(sys.argv[2]+"/SNPrawData/ukbbSNP_chr"+chrom+".bim",'r',encoding='utf-8')
        
        for snp in SNPdata:
            snp=snp.rstrip("\n").split("\t")
            SNParrayData.append(snp[0]+"\t"+chrom+"\t"+snp[2])
            flaggedSNPdata.append(snp[3])
    print("creating raw data instances (Baf, Lrr, SNP) per Chr in: " +str(round((time.time()-intime),2))+" sec")
    try:
        sampIdIntervalLower=int(sys.argv[1].split(":")[0])
        sampIdIntervalUpper=int(sys.argv[1].split(":")[1])
    except:
        sampIdIntervalLower=0
        sampIdIntervalUpper=len(IIDarrayData)

    for indice in range(sampIdIntervalUpper):
        bafData=[]
        lrrData=[]

        for BInstanceID in range(len(tabInstanceBAF)):
            bafData+=tabInstanceBAF[BInstanceID].readline().rstrip("\n").split("\t")
            lrrData+=tabInstanceLRR[BInstanceID].readline().rstrip("\n").split("\t")

        if indice%size==rank and indice>=sampIdIntervalLower and indice<sampIdIntervalUpper:
            intime=time.time()
            dataOut=open(sys.argv[3]+"/"+IIDarrayData[indice]+".txt",'w')
            dataOut.write("Name\tChr\tPosition\t"+IIDarrayData[indice]+".Log R Ratio\t"+IIDarrayData[indice]+".B Allele Freq\n")

            for j in range(len(bafData)):
                if flaggedSNPdata[j]!="out":
                    dataOut.write(SNParrayData[j]+"\t"+lrrData[j]+"\t"+bafData[j]+"\n")
            dataOut.close()
            print("Data output for individual << "+IIDarrayData[indice]+" >> completed in: "+str(round((time.time()-intime),2))+" sec"+" by CPU rank id: "+str(rank))
        else:
            pass
    print("CPU rank process total time: "+str(round((time.time()-cpuProcessTime),2))+" sec")


createFinalReportFromTransposeData()
