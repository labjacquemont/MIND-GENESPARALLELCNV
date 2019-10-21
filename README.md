### Mind&GenesParallelCNV

<p align="center">
  <img src="images/MindGeneslogo.png" height= "80" width="1500" alt="accessibility text">
</p>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3497400.svg)](https://doi.org/10.5281/zenodo.3497400)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/MartineauJeanLouis/MIND-GENESPARALLELCNV.git/master)[![CircleCI](https://circleci.com/gh/MartineauJeanLouis/MIND-GENESPARALLELCNV.svg?style=svg)](https://circleci.com/gh/MartineauJeanLouis/MIND-GENESPARALLELCNV)

#### Description
Mind-GenesParallelCNV is freeware tool which mainly implemented to compute CNV calling parallel tasks in the most efficient method. The tool is design to make the command lines as much easier and simple as possible so that researchers form different informatics background level can integrate it in their research project. Also, It has been built to make the parallel tasks possible to be executed on any type of computer including desktops. The tools only work on linux64 for the moment. Other than focusing on calling CNV in parallel, the tool is meant to help detecting CNV using several type of callers based on different algorithms (implementation language may differ between algos). For the moment, the tool generates parallel calls from PennCNV and QuantiSNP, but other CNV caller such as IPattern, BCFtools, FastSeg, DNAcopy, etc will be implemented very soon so that better consensus results can be made available.

As indicated Mind&GenesParallelCNV is a freeware and opensource linux based tool, and users are free to suggest any improvement of it, and eventually digital and intellectual property laws are applied. Therefore, reference should be cited if this tool, any tools from this repo or any crosslinked tools from this repo  have been used in reasearch publication.

To know more about our lab research or our team, please reach the following link: http://www.minds-genes.org/

Author: Martineau Jean-Louis
contact: 
* matineau.jean-louis@umontreal.ca 
* martineau.jean-louis@recherche-ste-justine.qc.ca

This tool is implemented as collaboration to LabJacquemont

### Install Mind&GenesParralelCNV
```bash
git clone https://github.com/MartineauJeanLouis/MIND-GENESPARALLELCNV.git
cd MIND-GENESPARALLELCNV
```
Follow the following link for a complete tutorial on the tools functionalities.
https://martineaujeanlouis.github.io/MIND-GENESPARALLELCNV/

#### Reference
```text
1) Huguet G, Schramm C, Douard E, Jiang L, Labbe A, Tihy F, Mathonnet G, Nizard S, Lemyre E, Mathieu A, Poline JB, Loth E, Toro R, Schumann G, Conrod P, Pausova Z, Greenwood C, Paus T, Bourgeron T, Jacquemont S; IMAGEN Consortium. Measuring and Estimating the Effect Sizes of Copy Number Variants on General Intelligence in Community-Based Samples. JAMA Psychiatry. 2018 May 1;75(5):447-457. doi: 10.1001/jamapsychiatry.2018.0039. PubMed PMID: 29562078; PubMed Central PMCID:PMC5875373
2) Wang K, Li M, Hadley D, Liu R, Glessner J, Grant S, Hakonarson H, Bucan M. PennCNV: an integrated hidden Markov model designed for high-resolution copy number variation detection in whole-genome SNP genotyping data Genome Research 17:1665-1674, 2007
3) Diskin SJ, Li M, Hou C, Yang S, Glessner J, Hakonarson H, Bucan M, Maris JM, Wang K. Adjustment of genomic waves in signal intensities from whole-genome SNP genotyping platforms Nucleic Acids Research 36:e126, 2008
4) Wang K, Chen Z, Tadesse MG, Glessner J, Grant SFA, Hakonarson H, Bucan M, Li M. Modeling genetic inheritance of copy number variations Nucleic Acids Research 36:e138, 2008
5) Colella, S.,* Yau, C.,* Taylor, J.M., Mirza, G., Butler, H., Clouston, P., Basset, A.S., Seller, A., Holmes, C., and Ragoussis, J. QuantiSNP: an Objective Bayes Hidden-Markov Model to detect and accurately map copy number variation using SNP genotyping data. Nucleic Acids Research, 35(6):2013-2025 2007
```