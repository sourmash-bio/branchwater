# Mastiff CLI client

## Installation

### MacOS (Apple Silicon)

```
curl -o mastiff -L https://github.com/sourmash-bio/mastiff/releases/latest/download/mastiff-client-aarch64-apple-darwin
chmod +x mastiff
```

### MacOS (Intel)

```
curl -o mastiff -L https://github.com/sourmash-bio/mastiff/releases/latest/download/mastiff-client-x86_64-apple-darwin
chmod +x mastiff
```

### Linux (arm)

```
curl -o mastiff -L https://github.com/sourmash-bio/mastiff/releases/latest/download/mastiff-client-arm-unknown-linux-gnueabihf
chmod +x mastiff
```

### Linux (x86_64)

```
curl -o mastiff -L https://github.com/sourmash-bio/mastiff/releases/latest/download/mastiff-client-x86_64-unknown-linux-musl
chmod +x mastiff
```

### Windows (x86_64)

```
Invoke-WebRequest -Uri 'https://github.com/sourmash-bio/mastiff/releases/latest/download/mastiff-client-x86_64-pc-windows-msvc.exe' -OutFile mastiff
```

## Examples

### From sequencing data

```
./mastiff sequences.fa.gz > matches.csv 
```

### From sequencing data, piping input

```
cat sequences.fa | ./mastiff -o matches.csv -
```

### Using an existing sig

Note: sig needs to be built using `k=21`, `scaled=1000`

```
./mastiff --sig -o matches.csv \
  <(curl -sL https://wort.sourmash.bio/v1/view/genomes/GCF_000195915.1)
```

## Available options

```
USAGE:
    mastiff [OPTIONS] <SEQUENCES>

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

