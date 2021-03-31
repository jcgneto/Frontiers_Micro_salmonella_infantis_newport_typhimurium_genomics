#!/bin/bash
#SBATCH --job-name=fasttree
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --array=1-20
#SBATCH --time=168:00:00
#SBATCH --mem=70gb
#SBATCH --partition=tmp_anvil,batch,benson
#SBATCH --licenses=common

module load fasttree/2.1 

export OMP_NUM_THREADS=${SLURM_NTASKS_PER_NODE}
# /work/benson/netogomes/pegasus/pegasus-salmonella-typhimurium-hcc/roary_fastbaps_groups/roary_output_gr1/core_gene_alignment.aln
IN="/work/benson/netogomes/pegasus/pegasus-salmonella-typhimurium-hcc/roary_fastbaps_groups/"
FastTreeMP -nt -pseudo -fastest < ${IN}/roary_output_gr${SLURM_ARRAY_TASK_ID}/core_gene_alignment.aln > typhimurium_phylogeny_gr${SLURM_ARRAY_TASK_ID}.tree
