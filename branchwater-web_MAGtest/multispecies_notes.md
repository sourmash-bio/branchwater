*workflow for testing species in branchwater web. Summary outputs tracked in multispecies__tracking.xlsx*

# branchwater-web

- sequentially uploaded refseq genomes and downloaded default output

- Opted for .4 containment (~0.97 cANI) cutoff for Aca, Asp, Can, Crys

- Low numbers for Folsomia candida and it has a large genome, so 0.34  containment (0.95 cANI) threshold chosen to capture at least 3 sra accessions

- basic output/metadata pasted into multispecies_tracking.xlsx

## nf-core/fetchngs (12/11/23)

1. WD: /project/90daydata/gbru_fy23_branchwater/multispecies/fetch.

2. `nano multispeciessra.csv` - pasted sra accession list from multispecies_tracking.xlsx_

3. ``nextflow run nf-core/fetchngs -profile cluster --cpu_max --input multispeciessra.csv --outdir multi_fastq --force_sratools_download -bg --email suzanne.fleishman@usda.gov --nf_core_pipeline rnaseq -resume``

## nf-core/mag (12/11/23)

- removed previous issue sample that led to unsolvable error in preliminary test: ERX4889432_ERR5083269.fastq.gz

- Downloaded 'samplesheet.csv'

- Edited to SE and PE

- uploaded new SE and PE csv lists

## -- SE

`nextflow run nf-core/mag --input /project/90daydata/gbru_fy23_branchwater/multispecies/SE/paths_SE.csv --outdir SE_out_2 --email suzannemfleishman@gmail.com --binning_map_mode own --single_end -bg`

## -- PE

`nextflow run nf-core/mag --input /project/90daydata/gbru_fy23_branchwater/multispecies/PE/paths_PE.csv --outdir PE_out --email suzannemfleishman@gmail.com --binning_map_mode own -bg`



### mag output

    1258 bins total from all accessions

## Taxonomic Match with bbmap/sendsketch (12/13/23)

1. copied SE and PE bins to local: ./sendsketch/multi/bins

2. created mapping excel sheet from bin names, columns for accession, genus, and species

3. bash script:
   
   1. Run sendsketch on a bin
   
   2. if bin matches accession and genus, save output to sort.txt
   
   3. if bin does not, save output to other.txt

4. saved output

5. added match level to multispecies_tracking.xlsx

WD:./sendsketch

multi_ss.sh

```bash
#!/bin/bash

FILES=./sendsketch/multi/bins/*
MAP=./sendsketch/multi/multi_mapping.csv

for f in $FILES; do
  output=$(bbmap/sendsketch.sh in="$f" refseq)
  match_found=0

  while read -r line && [[ $match_found -eq 0 ]]; do
    col1=$(echo "$line" | cut -d ',' -f 1)
    col2=$(echo "$line" | cut -d ',' -f 2)
    output_file="multi/$col2.txt"
    touch "$output_file"

    if echo "$output" | grep -q "$col1" && echo "$output" | grep -q "$col2"; then
      echo "$output" >> "$output_file"
      echo "$f,yes" >> multi/sort.txt
      match_found=1
    fi
  done < "$MAP"

  if [[ $match_found -eq 0 ]]; then
    echo "$output" >> multi/other.txt
    echo "$f,no" >> multi/sort.txt
  fi
done
```

`nohup bash multi_ss.sh > output.log 2>&1 &`
