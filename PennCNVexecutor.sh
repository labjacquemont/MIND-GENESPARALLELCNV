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

detectCNV="$1/detect_cnv.pl"
MINLENGTH=1000
MINCONF=15.0
task=$8

# Conditional section to catch the user specified pennCNV function to execute
if [[ $task = "detect" ]]; then
input=$2
output=$3
pfb=$4
genderFile=$5
gcmodel=$6
hmm=$7
elif [[ $task = "hmm" ]]; then
list=$2
output=$3
pfb=$5
hmm=$4
elif [[ $task = "quality" ]]; then
input=$2
output=$3
pfb=$4
genderFile=$5
gcmodel=$6
hmm=$7
else
   echo "wrong pennCNV option provided"
fi

# pennCNV Function execution conditionaly to above
sampleFile=$(basename $input)
sampleID=${sampleFile%.S*t}
if [[ $task = "detect" ]]
then
perl $detectCNV --test \
              --hmmfile $hmm \
              --pfbfile $pfb $input \
              --logfile $output"/LOG_DATA/autosome"_"$sampleID"."log" \
              --output $output"/CNV_DATA/autosome"_"$sampleID.rawcnv" \
              --minlength $MINLENGTH \
              --minconf $MINCONF \
              --gcmodelfile $gcmodel
wait
perl $detectCNV --test \
              --hmmfile $hmm \
              --pfbfile $pfb $input \
              --logfile $output"/LOG_DATA/gonosome_X"_"$sampleID"."log" \
              --output $output"/CNV_DATA/gonosome_X"_"$sampleID.rawcnv" \
              --minlength $MINLENGTH \
              --minconf $MINCONF \
              --sexfile $genderFile \
              --gcmodelfile $gcmodel \
              --chrx;
wait
elif [[ $task = "hmm" ]]
then
$detectCNV --train --pfbfile $pfb --listfile $list --hmmfile $hmm --out $output
elif [[ $task = "quality" ]]
then
perl $detectCNV --summary \
              --pfbfile $pfb $input \
              --logfile $output"/LOG_DATA/autosome"_"$sampleID"."log"
else
   echo "wrong pennCNV option provided"
fi

