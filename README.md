# branchwater

[branchwater](https://dib-lab.github.io/2022-paper-branchwater-software/)
is a new search index for sourmash signatures,
allowing near real-time search of large scale databases.
It is an inverted index implemented on top of [RocksDB](https://rocksdb.org).

This repo acts as a monorepo for the tools developed for using this new index:
- [branchwater-api](https://branchwater-api.jgi.doe.gov/search),
  a search index for ~946,000 SRA metagenomes.
- [branchwater-web](https://branchwater.jgi.doe.gov),
  a webapp for summarizing search results in interactive tables,
  plots, and maps.

## webapp

The webapp takes a genome of interest and rapidly searches for publicly-available 
metagenomes within NCBI's [sequence read archive](https://www.ncbi.nlm.nih.gov/sra)
with branchwater.
Metadata associated with the metagenome accessions are summarized in interactive tables,
plots, and maps.

Please note that this app is currently in development and may not be fully functional or feature-complete.

### License information

This app was originally created by the United States Department of Agriculture -
Agricultural Research Service (USDA-ARS). As a work of the United States Government,
this software is available under the CC0 1.0 Universal Public Domain Dedication (CC0 1.0)

### About us

This app was developed by the USDA Agricultural Research Service, Genomics and
Bioinformatics Research Unit group in Gainesville, FL. Code is authored primarily
by Suzanne Fleishman and led by Adam Rivers. Check out our other work at
https://tinyecology.com.

## CLI Client

See [the Client README](./crates/client/README.md) for more details.
