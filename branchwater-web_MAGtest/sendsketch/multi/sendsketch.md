### Taxonomic Match Analysis with BBMAP(12/13/23)

1. copied SE and PE bins to computer: ./sendsketch/multi/bins

2. created mapping excel sheet, columns for accession, genus, and species

3. edited bash file to do the following:
   
   1. Run sendsketch on a bin
   
   2. if bin matches accession and genus, save output to sort.txt
   
   3. if bin does not, save output to other.txt

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


