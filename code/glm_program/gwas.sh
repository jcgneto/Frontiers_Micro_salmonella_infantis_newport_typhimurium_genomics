#!/bin/bash
#SBATCH --job-name=fsis_gwas
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=168:00:00
#SBATCH --mem=50gb

module load anaconda 
conda activate statsmodels 

# cgmlst phenotype
python gwas_main_cgmlst.py phenotype.csv gene_presence_absence.Rtab "response" group gene_gwas_cgmlst_filtered.csv gene_gwas_cgmlst_no_filtered.csv "Gene"
