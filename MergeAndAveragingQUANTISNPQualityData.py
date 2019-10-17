#  @author: Martineau jean-Louis
#  This CNV call pipeline is dedicated to call detect CNV through both 
#  QuantiSNP and PennCNV algorithm. More algorithm cnv calls will be added
#  such as Ipattern, bcftools, DNAcopy and fastSeg. this version is release
#  on October 4th 2019 and will be updated very often. Any code optimization
#  and CNV calling algorith suggestion are welcome.

#  As part of the JacquemontLab, I provide sharing permission and rigth for 
#  collaborators and lab group members to share algorithm and code contents
#  of the pipeline as long as the digital and intellectual contents policies
#  are respected.

# @parameter 1: input directory path to the quantiSNP results
# @parameter 2: output path to the file where the results should be stored

import os, glob,sys
import statistics


def main():
	header="Sample ID\tChromosome\tOutlier Rate.mean\tStd.Dev.LRR.mean\tStd.Dev.BAF.mean\tGender"
	print(header)
	for i in glob.glob(str(sys.argv[1])+"/*.qc"):
		outR=[]
		meanOutR=0
		stLRR=[]
		meanStLRR=0
		stBAF=[]
		meanStBAF=0
		gender=""
		chr=""
		id=""
		fo = open(i,'r')
		for j in fo:
			j=j.rstrip("\n").split("\t")
			if j[0] != "Sample ID":
				outR.append(float(j[2]))
				stLRR.append(float(j[3]))
				stBAF.append(float(j[4]))
				id=j[0]
				chrom="All"
				gender=j[5]
		
		meanOutR=round(statistics.mean(outR),5)
		meanStLRR=round(statistics.mean(stLRR),5)
		meanStBAF=round(statistics.mean(stBAF),5)
                try:
		    outfile.write(id+"\t"+chrom+"\t"+str(meanOutR)+"\t"+str(meanStLRR)+"\t"+str(meanStBAF)+"\t"+gender+"\n")
		except:
                    print("infinite or non numeric value found for stat results")
main()
