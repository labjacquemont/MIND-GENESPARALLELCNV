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

@1st param: Illumina beadstudio input matrix of multisample
@2nd param: List of samples that the user want to extract (the list must contain only the ID and one ID per line)
@3rd param: Output directory where the user want to save the splitted data
@4th param: A SNP list data which contains the snps which will be extracted from each individual (extraction and snp filtering at the same time) 
"""

import sys,os

def main():
    
    bigFile=sys.argv[1]
    listSample=sys.argv[2]
    outDir=sys.argv[3]
    snpList=sys.argv[4]
    TabSamples=[]
    SNPdic={}
    BAF=0
    LRR=0
    for i in open (bigFile, 'r', encoding='utf-8'):
        i=i.rstrip("\n").split("\t")
        if i[0]=="Sample ID":
            BAF=i.index("B Allele Freq")
            LRR=i.index("Log R Ratio")
            break

    for line in open(snpList,'r',encoding='utf-8'):
        line=line.rstrip("\n").split("\t")
        SNPdic[line[1]+"_"+line[2]]=line[0]
        
    for i in open(listSample,'r',encoding='utf-8'):
        i=i.rstrip("\n")
        TabSamples.append(i)
    TabCreatedData=[]
    outFile=""
    outData=None
    
    dataOpen=open(bigFile, 'r', encoding='utf-8')
    for line in dataOpen:
        line=line.rstrip("\n").split("\t")
        if len(line)==17:
            key=line[1]+"_"+line[2]
            outFile=outDir+"/"+line[0]+".txt"
            if os.path.isfile(outFile)==False:
                try:
                    outData.close()
                    if len(TabCreatedData)==len(TabSamples):
                        return
                except:
                    pass

            if os.path.isfile(outFile)==False and line[0] in TabSamples:
                TabCreatedData.append(line[0])
                
                outFile=outDir+"/"+line[0]+".txt"
                print("Generating final report for sample: "+line[0]+"...")
                outData=open(outFile,'w',encoding='utf-8')
                outData.write("Name\tChr\tPosition\t"+line[0]+".Log R Ratio\t"+line[0]+".B Allele Freq\n")
                if line[1] not in ["MT","XY","Y","0"]:
                    outData.write(SNPdic[key]+"\t"+line[1]+"\t"+line[2]+"\t"+line[LRR]+"\t"+line[BAF]+"\n")

            elif os.path.isfile(outFile)==True and line[0] in TabSamples:
                if line[1] not in ["MT","XY","Y","0"]:
                    outData.write(SNPdic[key]+"\t"+line[1]+"\t"+line[2]+"\t"+line[LRR]+"\t"+line[BAF]+"\n")
            else:
                pass


main()
