# branchwater

This is the central repository for branchwater.

branchwater is the framework we use for searching large collections of sequencing data with genome-scale queries.
At its core it is a new search index for sourmash signatures,
allowing near real-time search of large scale databases.
It is an inverted index implemented on top of [RocksDB](https://rocksdb.org).

You can read more about branchwater in [Sourmash Branchwater Enables Lightweight Petabyte-Scale Sequence Search, Irber et al., 2022](https://www.biorxiv.org/content/10.1101/2022.11.02.514947v1), and you can read about one of the earliest use cases in [Biogeographic Distribution of Five Antarctic Cyanobacteria Using Large-Scale k-mer Searching with sourmash branchwater, Lumian et al., 2022](https://www.biorxiv.org/content/10.1101/2022.10.27.514113v1).

branchwater had a couple of names over time:
- [sra_search](https://github.com/sourmash-bio/sra_search)
- [MAGsearch](https://github.com/ctb/magsearch)
- [rocksdb-eval](https://github.com/luizirber/2022-06-26-rocksdb-eval)
- [mastiff](https://github.com/sourmash-bio/mastiff)

ae finally brought it all together under the same umbrella named 'branchwater'!

Here are a few blog posts:
* [MinHashing all the things: searching for MAGs in the SRA](https://blog.luizirber.org/2020/07/22/mag-search/)
* [MinHashing all the things: a quick analysis of MAG search results](https://blog.luizirber.org/2020/07/24/mag-results/)
* [Searching all public metagenomes with sourmash](http://ivory.idyll.org/blog/2021-MAGsearch.html)
* Discussion for the initial prototype for [real time search of the SRA](http://ivory.idyll.org/blog/2022-sourmash-mastiff.html)

## Code repository links and details.

branchwater is based on [sourmash](https://github.com/dib-lab/sourmash/issues),
and the search index data structure lives there since
[version `0.12`](https://crates.io/crates/sourmash/0.12.0) of the Rust crate.

branchwater is currently (Jan 2024) mostly contained in this repo,
with the tools developed to work with the new index:

- [branchwater-api](https://branchwater-api.jgi.doe.gov/search),
  a search server indexing ~946,000 SRA metagenomes.
- [branchwater-web](https://branchwater.jgi.doe.gov),
  a webapp that takes a genome of interest and rapidly searches for publicly-available
  metagenomes within NCBI's [sequence read archive](https://www.ncbi.nlm.nih.gov/sra)
  with branchwater.
  Metadata associated with the metagenome accessions are summarized in interactive tables,
  plots, and maps.
- `branchwater-index`,
  a command-line interface to build the search index.
  See [the Query README](./crates/client/README.md) for more details.
- `branchwater-query`,
  a command-line interface to submit queries to a search server.

There are also additional resources external to this repository:

* The code for monitoring the SRA and building sourmash sketches from genomes and metagenomes is in [wort](https://github.com/sourmash-bio/wort).
* [sourmash_plugin_branchwater](https://github.com/sourmash-bio/sourmash_plugin_branchwater) is a sourmash plugin exposing more features from branchwater in sourmash.

## Need help? Have questions? Want to make a suggestion?

Please file branchwater-specific issues and pull requests [in the branchwater repo](https://github.com/sourmash-bio/branchwater/).
We also hang out in [the sourmash repo](https://github.com/sourmash-bio/sourmash/issues) a lot,
if you have more general questions about sourmash.
And there's a [gitter/matrix channel](https://github.com/sourmash-bio/sourmash/issues/1686) where you can contact a number of the
sourmash collaborators.

## License information

branchwater is [AGPL licensed](./LICENSE-AGPL).

The webapp was developed by the USDA Agricultural Research Service,
Genomics and Bioinformatics Research Unit group in Gainesville, FL,
and was primarily authored by Suzanne Fleishman in a project led by
Adam Rivers.  Check out their other work at https://tinyecology.com.
As a work of the United States Government, the original code is
available under the CC0 1.0 Universal Public Domain Dedication (CC0
1.0) at https://github.com/USDA-ARS-GBRU/branchwater-web/.
