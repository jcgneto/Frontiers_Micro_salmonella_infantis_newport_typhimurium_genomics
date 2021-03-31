#!/bin/bash
#SBATCH --job-name=snp-dists
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --array=1-20
#SBATCH --time=168:00:00
#SBATCH --mem=70gb
#SBATCH --partition=tmp_anvil,batch,benson

module load snp-dists/0.7

# /work/benson/netogomes/pegasus/pegasus-salmonella-typhimurium-hcc/roary_fastbaps_groups/roary_output_gr1/core_gene_alignment.aln
IN="/work/benson/netogomes/pegasus/pegasus-salmonella-typhimurium-hcc/roary_fastbaps_groups/"
snp-dists -b -c ${IN}/roary_output_gr${SLURM_ARRAY_TASK_ID}/core_gene_alignment.aln > distace_snp_sites_${SLURM_ARRAY_TASK_ID}.tsv
