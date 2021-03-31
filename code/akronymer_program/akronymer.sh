#!/bin/bash
#SBATCH --job-name=jejuni_akronymer
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=168:00:00
#SBATCH --mem=50gb
#SBATCH --partition=benson,batch,tmp_anvil
#SBATCH --licenses=common

# export OMP_NUM_THREADS=8
# awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < input.aln
# sed -i -e "1d" input.file

<<COMM
for i in {1..20}
do
echo $i
# /common/deogun/npavlovikj/public/pegasus-campylobacter-jejuni-hcc/slurm/roary_output_95_95_1/core_gene_alignment.aln
awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < /common/deogun/npavlovikj/public/pegasus-campylobacter-jejuni-hcc/slurm/roary_output_95_95_${i}/core_gene_alignment.aln | sed -e "1d" > jejuni_gr${i}.aln
done
COMM

for j in jejuni_gr*.aln
do
echo $j
../bin/akmer94b_linux ${j} ${j}_output
done
