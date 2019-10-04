#!/bin/bash

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

quantiSNPbaseLoc=$4
levelsData=$5
inDir=$1
outBaseDir=$2
genderFile=$3
EMITERS="10"
LSETTING="2000000"
GCDIR="$quantiSNPbaseLoc/b37"
SUBSAMPLELEVEL="1"
PARAMSFILE="$quantiSNPbaseLoc/quantisnp/config/params.dat"
LEVELSFILE=$levelsData 
CHRX="23"
CHRRANGE="1:23"
MCRROOT="$quantiSNPbaseLoc/v79"

echo $inDir
echo $genderFile

samplefile=$(basename $inDir)
genderVar=$(grep -w "Name" $inDir | cut -f 4 | cut -d"." -f 1)
INFILE=$inDir
OUTDIR=$outBaseDir/$genderVar.outdir
SAMPLEID=$genderVar
GENDER=$(grep -w $genderVar $genderFile | cut -f2)
QUANTISNP="$quantiSNPbaseLoc/quantisnp/linux64/run_quantisnp2.sh"
mkdir -p $OUTDIR 
$QUANTISNP $MCRROOT --chr $CHRRANGE --outdir $OUTDIR --sampleid $SAMPLEID --isaffy \
--gender $GENDER --emiters $EMITERS --lsetting $LSETTING --gcdir $GCDIR --config $PARAMSFILE \
--levels $LEVELSFILE --input-files $INFILE --chrX $CHRX --doXcorrect
wait

