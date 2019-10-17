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

# PennCNV installation is required for this script
# module load PennCNV/jun162011

config=$1
PennCNV=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="PennCNV"){print $2}}')
SNPs=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="SNPs"){print $2}}')
calls=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="calls"){print $2}}')
confidence=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="confidence"){print $2}}')
summary=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="summary"){print $2}}')
output=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="output"){print $2}}')

call=$calls
conf=$confidence
sum=$summary
out=$output
mkdir -p $out

cluster="$PennCNV/affy/bin/generate_affy_geno_cluster.pl"
norm="$PennCNV/affy/bin/normalize_affy_geno_cluster.pl"
kcol="$PennCNV/kcolumn.pl"

SNPs=SNPs





$cluster --nopower2 --locfile $SNPs $call $conf $sum --output $out/call.cluster
wait
$norm $out/call1.cluster $sum --nopower2 --locfile $SNPs --output $out/call_lrr_baf.txt
wait
$kcol $out/call1_lrr_baf.txt split 2 -tab -head 3 -name -out $out/call
