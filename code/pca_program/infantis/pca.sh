#!/bin/bash
#SBATCH --job-name=pca_1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=168:00:00
#SBATCH --mem=250gb
#SBATCH --partition=benson,tmp_anvil,batch
#SBATCH --licenses=common

module load anaconda
# conda activate statsmodels
conda activate pca_env

Rscript logistic_pca_clustering_program.R

conda deactivate
