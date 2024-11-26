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
USAGE:
    branchwater-client [OPTIONS] <SEQUENCES>

ARGS:
    <SEQUENCES>    Input file. Can be:
                     - sequences (FASTA/Q, compressed or not)
                     - an existing signature (use with --sig)
                     - a single dash ("-") for reading from stdin

OPTIONS:
    -h, --help               Print help information
    -o, --output <OUTPUT>    Save results to this file. Default: stdout
        --sig                Input file is already a signature
    -V, --version            Print version information
```

