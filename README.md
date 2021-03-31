# Project

Population genomics project for three serovars of *Salmonella enterica* Lineage I -> Infantis, Newport, and Typhimurium.

## Goal

Heuristic mining of publicly available genomics dataset to achieve the following goals:

* Using hierarchical-based population structure analysis to mapping pangenomes for loci discovery and trait prediction
* Identification of novel hidden variants or potential ecotypes within each population of serovar

### Methods

The computational platform ProkEvo was used for processing of paired-end Illumina raw sequences to generate the following outputs: 
core-genome alignment, BAPS, MLST, SISTR, AMR mapping, plasmid identification, and pangenome annotation. 
FasTree was used to construct core-genome phylogenies. 
AKronyMer was used to construct a pairwise distance matrix between bacterial genomes using the core-genome information as input. More information about Akronymer 
can be found here (https://github.com/knights-lab/aKronyMer). 
Parameters set in ProkEvo are provided here ( ).
All data mining and statiscal modeling were done using custom R and python scripts. 

### Results 

Here are two major findings of this work:

1. The combination of a hierarchical-based population structure annd pangenome-enrichment analysis allows for identification of unique loci preferentially found on specific ST clonal complex within a serovar. Phenotypic predictions can then be made and validated with laboratorial testing. 
2. Mining of the entire pangenome allows for identification of specific hidden sub-populations or variants that would not have been possible with BAPS, ST, or cgMLST based classifications produced with SISTR. 

### Implications 

There are two major implications or actionable knowledge that can be learned from this work:

1. Trait discovery may result in finding specific ways of mitigate pathogens across the food chain. 
2. Identification of previously unknown sub-population or variants can inform Public Health agencies for enhance epidemiological surveillance. 

### Journal

Collection on Using Genomics to Inform Food Safety Inspection Systems in Frontiers in Sustainable Food Systems - section Agro-Food Safety.
