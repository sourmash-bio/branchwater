# branchwater CLI client

## Installation

### MacOS (Apple Silicon)

```
curl -o branchwater -L https://github.com/sourmash-bio/branchwater/releases/latest/download/branchwater-client-aarch64-apple-darwin
chmod +x branchwater
```

### MacOS (Intel)

```
curl -o branchwater -L https://github.com/sourmash-bio/branchwater/releases/latest/download/branchwater-client-x86_64-apple-darwin
chmod +x branchwater
```

### Linux (arm)

```
curl -o branchwater -L https://github.com/sourmash-bio/branchwater/releases/latest/download/branchwater-client-arm-unknown-linux-gnueabihf
chmod +x branchwater
```

### Linux (x86_64)

```
curl -o branchwater -L https://github.com/sourmash-bio/branchwater/releases/latest/download/branchwater-client-x86_64-unknown-linux-musl
chmod +x branchwater
```

### Windows (x86_64)

```
Invoke-WebRequest -Uri 'https://github.com/sourmash-bio/branchwater/releases/latest/download/branchwater-client-x86_64-pc-windows-msvc.exe' -OutFile branchwater
```

## Examples

### From sequencing data

```
./branchwater sequences.fa.gz > matches.csv 
```

### From sequencing data, piping input

```
cat sequences.fa | ./branchwater -o matches.csv -
```

### Using an existing sig

Note: sig needs to be built using `k=21`, `scaled=1000`

```
./branchwater --sig -o matches.csv \
  <(curl -sL https://wort.sourmash.bio/v1/view/genomes/GCF_000195915.1)
```

## Available options

```
USAGE:
    branchwater [OPTIONS] <SEQUENCES>

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

