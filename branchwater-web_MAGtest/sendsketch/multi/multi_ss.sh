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
