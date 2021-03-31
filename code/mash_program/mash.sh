#!/bin/bash
#SBATCH --job-name=mash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=168:00:00
#SBATCH --mem=3gb
#SBATCH --partition=benson,batch,tmp_anvil
#SBATCH --licenses=common

module load mash/2.2

# reference is downloaded from https://www.ncbi.nlm.nih.gov/nuccore/NZ_CP016408.1

mash dist infantis_ref_sequence.fasta -l infantis_genomes_filtered.txt -t >> ref_infantis_table.csv

<<COMM
Output cleanup:
sed -i 's/\/common\/deogun\/npavlovikj\/public\/pegasus-salmonella-infantis-hcc\/data_tmp\///g' ref_infantis_table.csv
sed -i 's/_contigs.fasta//g' ref_infantis_table.csv
sed -i 's/#query/id/g' ref_infantis_table.csv
sed -i 's/infantis_ref_sequence.fasta/distance/g' ref_infantis_table.csv
COMM
