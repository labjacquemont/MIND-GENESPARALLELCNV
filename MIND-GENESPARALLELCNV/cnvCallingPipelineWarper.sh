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

#  Understanding the parametters
#  the parametters are capture by the $param rank

#  ----------------- This is a wrapper script ------------------
#  There are 2 categories of parameters which this wrapper input to the pipeline
#  the first categorie are those that the user enter manually before executing the pipeline
#  and the second ones are those that are read from the config file and input to the pipeline.
 
#  taking for account the below provided parameters, only the batch ID (6th), number of process (2nd)
#  , the list fraction (5th), path/file link to the confige file (usualy in the same folder is better),
#  boolean(compute pennCNV = True or False)(13th), boolean(compute quantiSNP = True or False)(14th), and
#  finally, pennCNV task to execute (values are: detect, hmm or quality), and is only effective when
#   pennCNV boolean parametter is set to True.    


#  @1st parametter: Raw signal files combined in a list with their paths and the files.
#    the list is provided as argument 1
#  @2nd parameter: the number of parallel task provided by the user
#  @3rd parametter: is the output folder location for the pennCNV cnv calls results
#  @4th parametter: is the output folder location for the quantiSNP cnv calls results  
#  @5th parameter: is a specific interval fraction of the dataset that the user want to 
#    call CNV for, if one need to call cnv on the whole list then use the followin parametter
#    0-all
#  @6th is the batch id prefix for the cohort subset, if one haven't create subset for the
#    projet dataset, then use 0 as prefix, therefor the results will be expected on folder
#    named BATCH_00
#  @7th parametter: The quantisnp executor script provided on this pipeline bundle
#  @8th parametter: The pennCNV executor script provided on this pipeline bundle
#  @9th parametter: The sex file data localisation link, required by pennCNV and quantiSNP
#  @10th parametter: The pfb file localisation link, required by pennCNV and quantiSNP
#  @11th parametter: The gcmodel file file localisation link, required only for pennCNV
#  @12th parametter: The hmm file file localisation link, required only for pennCNV
#  @13th parametter: Is a boolean parametter to switch on/off the pennCNV calling process
#                    the values are True or False
#  @14th parametter: Is a boolean parametter to switch on/off the quantiSNP calling process
#       	     the values are True or False
#  @15th parametter: Directory path to the pennCNV installation
#  @16th parametter: Directory path to the quantiSNP installation
#  @17th parametter: The levels data file file localisation link, required only for quantiSNP
#  @17th parametter: PennCNV taskk to be executed, the below task are only active when pennCNV
#                    execution is set to True: 
#                    detect  (to run the cnv detection by pennCNV)
#                    hmm     (to compute the training of the hmm file for a specific cohort)
#                    quality (to compute only the summary quality of the samples)


# Before running this wrapper, we assume the the user already install anaconda python3.X 
# and mpy4py module is install as indicated in the readme
  
source $HOME/.bashrc
config=$4
QuantiSNPscript=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="QuantiSNPscript"){print $2}}')
PennCNVscript=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="PennCNVscript"){print $2}}')
sex=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="sex"){print $2}}')
pfb=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="pfb"){print $2}}')
gcmodel=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="gcmodel"){print $2}}')
outputQuant=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="outputQuant"){print $2}}')
outputPenn=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="outputPenn"){print $2}}')
pyScript=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="pyScript"){print $2}}')
inputBaseDir=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="inputBaseDir"){print $2}}')
hmm=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="hmm"){print $2}}')
hmmOut=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="hmmtrainOut"){print $2}}')
hmmList=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="hmmList"){print $2}}')
pennCNVpath=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="pennCNVpath"){print $2}}')
quantiSNPpath=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="quantiSNPpath"){print $2}}')
levelsDATApath=$(cat $config | sed 's/\ //g;s/:/\t/g' | awk -F"\t" '{if($1=="levelsDATApath"){print $2}}')

mkdir -p $outputQuant
mkdir -p $outputPenn

input=$inputBaseDir/Batch$1.list.signal.txt
numtasks=$2
TabFactor=$3
batch=$1
doPenn=$5
doQuant=$6
pennTask=$7

if [[ $pennTask = "detect" ]]
then
mpirun -np $numtasks python3 $pyScript $input $numtasks $outputQuant $outputPenn $TabFactor $batch $QuantiSNPscript $PennCNVscript $sex $pfb $gcmodel $hmm $doPenn $doQuant $pennCNVpath $quantiSNPpath $levelsDATApath $pennTask;
elif [[ $pennTask = "hmm" ]]
then
bash $PennCNVscript $pennCNVpath $hmmList $hmmOut $hmm $pfb "na" "na" $pennTask
elif [[ $pennTask = "quality" ]]
then
mpirun -np $numtasks python3 $pyScript $input $numtasks $outputQuant $outputPenn $TabFactor $batch $QuantiSNPscript $PennCNVscript $sex $pfb $gcmodel $hmm $doPenn $doQuant $pennCNVpath $quantiSNPpath $levelsDATApath $pennTask
else
   echo "no cnv analysis option were selected"
fi

echo -e "All tasks terminated succesful!"
