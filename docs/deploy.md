# Deploying a new branchwater instance

Deploying a new `branchwater` instance involves bringing up a couple of components:
- `branchwater-web`, the web frontend at [https://branchwater.sourmash.bio](https://branchwater.sourmash.bio)
- `branchwater-server`, the backend serving the RocksDB inverted index for sourmash signatures
- a [duckdb](https://duckdb.org/) database for the SRA metadata used for
  `branchwater-web` results

A diagram of how these components are connected:

::: {mermaid}
graph LR;
classDef server fill:#4A902A,stroke:#333,stroke-width:4px,color:#fff;
classDef web fill:#dc6c11,stroke:#333,stroke-width:4px,color:#fff;
classDef index fill:#3c48cc,stroke:#333,stroke-width:4px,color:#fff;
classDef duckdb fill:#6980e9,stroke:#333,stroke-width:4px,color:#fff;
classDef client fill:#8450e1,stroke:#333,stroke-width:4px,color:#fff;

A01(browser):::client --> B01(web):::web
B01 --> C01(server):::server
B01 --> D01[(duckdb)]:::duckdb
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
cd branchwater
```

### Set up dependencies

We use [pixi](https://pixi.sh) for managing dependencies and running tasks for `branchwater` development,
you can install it with
```
curl -fsSL https://pixi.sh/install.sh | bash
```
or check updated instructions on their website.

For deploying a complete development or production environment,
we have a `docker-compose.yml` configuration describing the containers and how they connect together.
For using this configuration,
either `docker compose` or `podman-compose` is needed.
While there are many ways to get them installed,
on MacOS or Windows there are a couple of "Desktop" versions with a complete solution
(GUI, start services, configure networking) to make it easy to get started.

:::{note}
You only need one of `docker` or `podman`, no need to install both!
:::

::::{tab-set}

:::{tab-item} Docker Desktop

We recommend setting up [Rancher Desktop](https://rancherdesktop.io/)
for development with `docker compose`.
Follow instructions from their website to set it up for your operating system.

:::

:::{tab-item} Podman Desktop

[Podman Desktop](https://podman-desktop.io/) is the "Desktop" equivalent for Podman.
Follow instruction on their website to set it up for your operating system.

`pixi` tasks default to run with `docker compose`,
if you're using `podman` you need to update tasks to use
```
"podman-compose"
```
instead of
```
"docker compose"
```
especially in the `deploy` and `metadata` tasks.
Edit the `pixi.toml` file and replace entries accordingly.

:::

::::


### The demo dataset

The demo dataset included in the repo has the following SRA accessions:

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

They are listed in this file:
```
cat experiments/inputs/demo_sraids
```

You can modify and use other SRA accessions,
they were chosen just so we can see some results in the web frontend.

### Download signatures and prepare search index

The snakemake pipeline in `experiments/Snakefile` was prepared to
- download pre-calculated signatures for the SRA accessions in the demo dataset from [wort](https://wort.sourmash.bio),
- build a search index
- copy data into `bw_db/` so it can be used further ahead by the containers in `docker-compose.yml`

You can run the snakemake pipeline with
```
pixi run index -j 4
```
which will install all the dependencies needed and run snakemake.
You can adjust how many jobs are executed by changing `-j 4`.

This will create a `bw_db` directory at the root of the repository with the following structure:
```
bw_db
├── index/      # the branchwater search index
├── sigs.zip    # signatures indexed for search
└── sraids      # a list of SRA accessions to download signatures and build the index
```

### Prepare Metadata

::::{tab-set}

:::{tab-item} Using BiqQuery

#### Prepare a BigQuery access key

```{include} ../metadata/README.md
:start-after: <!-- start sra-metadata-access -->
:end-before: <!-- end sra-metadata-access -->
```

#### Checkpoint before metadata processing

This is how the `bw_db` directory at the root of the repository should look like:
```
bw_db
├── bqKey.json     # NEW: BigQuery credentials and Project ID
├── index/         # the branchwater search index
├── sigs.zip       # signatures indexed for search
└── sraids         # a list of SRA accessions to download signatures and build the index
```

#### Download the SRA metadata from bigquery

```
pixi run metadata_bq
```

:::

:::{tab-item} From SRA parquet in AWS Open Data

#### Checkpoint before metadata processing

This is how the `bw_db` directory at the root of the repository should look like:
```
bw_db
├── index/         # the branchwater search index
├── sigs.zip       # signatures indexed for search
└── sraids         # a list of SRA accessions to download signatures and build the index
```

#### Download the SRA metadata via parquet file

```
pixi run metadata_sra
```
```{note}
to build a smaller dataset for testing, run `pixi run metadata_sra_test`
```

### Load the metadata into duckdb
```
pixi run load_duckdb
```
```{note}
if reloading after switching from e.g. test db to full db, need to run:
`pixi run load_duckdb --force`
```

:::

::::

### Bring up search index and web frontend

```
pixi run deploy build app
pixi run deploy up -d app
```

Web frontend will be available at [http://localhost:8000](http://localhost:8000)
