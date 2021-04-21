#!/bin/bash
#SBATCH --job-name=metadata
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=15:00:00
#SBATCH --mem=13gb

module load entrez-direct/11.0

# ids.txt is a list of SRA IDs
for i in $(cat salmonella_infantis_sra.txt)

do

sra_id=${i}

host_disease=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "host disease" -element Attribute`
isolation_source=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "isolation_source" -element Attribute`

sleep 3
host=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "host" -element Attribute`
geo_loc=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "geo_loc_name" -element Attribute`

sleep 3
lat_lon=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "lat_lon" -element Attribute`
collection_date=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "collection_date" -element Attribute`

sleep 3
collected_by=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -block Attribute -if Attribute@attribute_name -equals "collected_by" -element Attribute`
title=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -if Title -first Title`

sleep 3
publication_date=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -if PublicationDate -first PublicationDate`
modification_date=`esearch -db sra -query ${sra_id} | elink -target biosample | efetch -format docsum | xtract -pattern DocumentSummary -if ModificationDate -first ModificationDate`

echo -e "$sra_id|$title|$publication_date|$modification_date|$host_disease|$isolation_source|$host|$geo_loc|$lat_lon|$collection_date|$collected_by" >> metadata_output.txt

done
