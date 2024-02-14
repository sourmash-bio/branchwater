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

## Bringing up branchwater with demo dataset

### Clone the repo

```
git clone https://github.com/sourmash-bio/branchwater
```

### Set up dependencies

```
pixi shell

```

### The demo dataset

```
cat buildmongo/sra.runinfo.csv
```
(will probably move this into `experiments/` instead?)

### Download signatures and prepare search index

```
pixi run index
```

### Bring up mongo for data loading

```
podman-compose up -d mongodb
```

### Download the SRA metadata from bigquery and load into mongo

```
pixi run metadata
```

### Bring up search index and web frontend

```
podman-compose up -d
```
