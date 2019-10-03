# CNV-calling
This pipeline is a warper tools which consist on helpping users to easily call CNV uppon array genotyping data, for example: illumina OMNI2.5, Infinium, or Affimetrix Axiom, genome wide 6.0 etc. The goal of this tool also consisted on helping users to call CNV in a high performance way, were all functions in the pipeline were optimized to use the least amount of computational (RAM) possible, to avoid generated the least possible temporary data, therefore, optimize the available storage space. Other than the scripts optimization, the pipeline is built to paralellize the jobs, meaning each individuals CNV calls is computing separatly in a single CPU core. To do so, openMP and mpi4py compiled with gcc base are required. The pipeline creates automaticaly all require folders, and both CNV calling algorithm results are store seperatly. The only human manual preprocesses that are require by the pipeline are:

1) Make sure gcc based (glibc 2.6 or higher) for openMP is installed, it's usually already preinstalled on the linux OS (ubuntu or CentOS)
-Link to rpm downloads-
https://pkgs.org/

2) Insure that python 3.X is available on the machine and the mpy4py module is installed, since many other statistical module might be required by the CNV calling tools, it might be recommended to install anaconda. 
-link to anaconda-
https://www.anaconda.com/distribution/

from anaconda bin directory istall: getuser and mpy4py module, mpi4py should be gcc based version and not INTEL. instead of using pip or python -m pip for module installation, it's recommended to use conda for the module installation, because conda will install not only the requested module but also all required dependencies and libraries to help the module work as expected.

Install mpi4py module

cd /path_to_anaconda_install_dir/bin/ , then hit
conda install -c conda-forge/label/gcc7 mpi4py

then follow the onscreen instruction. The above module is important for the task parallelisation.


3) Download and install PennCNV and QuantiSNP from the link below:
http://penncnv.openbioinformatics.org/en/latest/
https://github.com/WGLab/PennCNV

After compiling and install pennCNV according to the tool readme, it's important to compile the kext libraries located on the PennCNV installation folder. These libraries are usefull for self HMM training.

Most researchers are already aware that genotyping quality may varies between individuals from the same cohort but also between genotyping technologies. Therefore, training HMM data integrity may difer from one genotyping technology to another, and could have negative consequence on CNV calling results. To fix this problem, it's alway better to built specific HMM for fpecific cohort. 

4) Finaly, fill out the configuration file (.config file) with all required path and file path.
