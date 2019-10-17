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

call="/path_to_SNPcalls_file_from_AxiomeSuite/Axiome.calls.txt"
conf="/path_to_SNPconfidences_file_from_AxiomeSuite/Axiome.confidences.txt"
sum="/exec5/GROUP/lyon/lyon/BIG_FILES/DrJacquemontLAB/CaG_Genotyping_Axiom/Genotype_Affy_file/Axiom.summary.txt"
out="/path_to_output_results/Axiom_OUT_sigFile"
mkdir -p $out

cluster="/path_to_/PennCNV-1.0.5/affy/bin/generate_affy_geno_cluster.pl"
norm="/path_to_/PennCNV-1.0.5/affy/bin/normalize_affy_geno_cluster.pl"
kcol="/path_to_/PennCNV-1.0.5/kcolumn.pl"

SNPs="/path_to_the_project_SNP_file_directory_/project-SNPs_file.txt"





$cluster --nopower2 --locfile $SNPs $call $conf $sum --output $out/call.cluster
wait
$norm $out/call1.cluster $sum --nopower2 --locfile $SNPs --output $out/call_lrr_baf.txt
wait
$kcol $out/call1_lrr_baf.txt split 2 -tab -head 3 -name -out $out/call
