# Deploying a new branchwater instance

Deploying a new `branchwater` instance involves bringing up a couple of components:
- `branchwater-web`, the web frontend at [https://branchwater.sourmash.bio](https://branchwater.sourmash.bio)
- `branchwater-server`, the backend serving the RocksDB inverted index for sourmash signatures
- a [mongo](https://www.mongodb.com/) database for the SRA metadata used for
  `branchwater-web` results

A diagram of how these components are connected:

::: {mermaid}
graph LR;
classDef server fill:#4A902A,stroke:#333,stroke-width:4px,color:#fff;
classDef web fill:#dc6c11,stroke:#333,stroke-width:4px,color:#fff;
classDef index fill:#3c48cc,stroke:#333,stroke-width:4px,color:#fff;
classDef mongodb fill:#6980e9,stroke:#333,stroke-width:4px,color:#fff;
classDef client fill:#8450e1,stroke:#333,stroke-width:4px,color:#fff;

A01(browser):::client --> B01(web):::web
B01 --> C01(server):::server
B01 --> D01[(mongo)]:::mongodb
C01 --> E01[(index)]:::index
:::

Be it for development or production usage,
a [`docker-compose`](https://docs.docker.com/compose/)
configuration is [available in the repo](https://github.com/sourmash-bio/branchwater/blob/main/docker-compose.yml)
that can bring up these components in the appropriate order.

## Quickstart: branchwater with a demo dataset

### Clone the repo

```
git clone https://github.com/sourmash-bio/branchwater
```

### Set up dependencies

For development on macOS: https://podman-desktop.io/downloads
and follow instructions inside podman desktop to setup podman.


```
curl -fsSL https://pixi.sh/install.sh | bash
```

### The demo dataset

- [ERR272375](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=ERR272375&display=metadata), a salt marsh metagenome
- [SRR5439749](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR5439749&display=metadata), a human gut metagenome
- [SRR20285055](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR20285055&display=metadata), an air metagenome
- [SRR24480609](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR24480609&display=metadata), a gut metagenome
- [ERR3220185](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=ERR3220185&display=metadata), a bovine gut metagenome
- [SRR6269135](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR6269135&display=metadata), a marine metagenome
- [SRR25653600](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR25653600&display=metadata), a phage metagenome
- [SRR25021205](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR25021205&display=metadata), a soil metagenome
- [SRR25646998](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR25646998&display=metadata), a drinking water metagenome
- [SRR25611550](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR25611550&display=metadata),a food production metagenome
- [SRR7698815](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR7698815&display=metadata), a plant metagenome
- [SRR2243572](https://trace.ncbi.nlm.nih.gov/Traces/index.html?view=run_browser&acc=SRR2243572&display=metadata), a wastewater metagenome

```
cat experiments/inputs/sraids
```

### Download signatures and prepare search index

```
pixi run index
```

This will create a `bw_db` directory at the root of the repository with the following structure:
```
bw_db
├── index/      # the branchwater search index
├── sigs.zip    # signatures indexed for search
└── sraids      # a list of SRA accessions to download signatures and build the index
```

### Bring up mongo for data loading

After the index is build,
we can bring up the `mongodb` that will hold the metadata:
```
pixi run deploy up -d mongodb
```
It is empty initially,
so let's load the metadata next.

### Download the SRA metadata from bigquery and load into mongo

Need to setup bigquery
```
pixi run metadata
```

### Bring up search index and web frontend

```
pixi run deploy up -d
```
