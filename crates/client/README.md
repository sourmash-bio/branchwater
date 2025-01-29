# branchwater CLI client

## Installation

Follow the instructions from the [latest released version](https://github.com/sourmash-bio/branchwater/releases/latest)

### Manual installation



## Examples

### From sequencing data

```
branchwater-client sequences.fa.gz > matches.csv 
```

### From sequencing data, piping input

```
cat sequences.fa | branchwater-client -o matches.csv -
```

### Using an existing sig

Note: sig needs to be built using `k=21`, `scaled=1000`

```
branchwater-client --sig -o matches.csv \
  <(curl -sL https://wort.sourmash.bio/v1/view/genomes/GCF_000195915.1)
```

## Available options

```
Usage: branchwater-client [OPTIONS] <SEQUENCES>

Arguments:
  <SEQUENCES>  Input file. Can be:
                 - sequences (FASTA/Q, compressed or not)
                 - an existing signature (use with --sig)
                 - a single dash ("-") for reading from stdin

Options:
  -o, --output <OUTPUT>
          Save results to this file. Default: stdout
  -s, --server <SERVER>
          Server to query. Default: https://api.branchwater.sourmash.bio [default: https://api.branchwater.sourmash.bio]
  -m, --metadata-server <METADATA_SERVER>
          Metadata server to query. Default: https://branchwater.sourmash.bio [default: https://branchwater.jgi.doe.gov]
      --sig
          Input file is already a signature
      --full
          Return full results (containment plus matching dataset ID metadata)
      --retry <RETRY>
          How many times to retry requests to the server (default: 3) [default: 3]
  -h, --help
          Print help
  -V, --version
          Print version
```

