# Deploying the SRA metagenomes index

The [deployment for the demo database](deploy.md) is useful when a
new search index is built from zero,
but in case you want to use an existing branchwater database there is
a more direct way that skips the `wort` signature download and indexing into a branchwater database.

To demonstrate the process we will use the SRA metagenomes index from the [main instance](https://branchwater.sourmash.bio),
althought at a larger scaled value.
The `s=1000` index from the main instance is ~1.3 TiB as of 2024-11-28,
but we provide downsampled versions to `s=100,000` for `k={21,31,51}`,
containing the same `1,161,119` SRA metagenomes,
and they are easier to download and run locally:

- [`20241128-k21-s100000`](https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-k21-s100000/) (14.1 GiB)
- [`20241128-k31-s100000`](https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-k31-s100000/) (32.2 GiB)
- [`20241128-k51-s100000`](https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-k51-s100000/) (35.8 GiB)

:::{note}
These are the branchwater search index, they don't contain the signatures used to build the index.
This is mostly because
- we only need the index to run the branchwater service
- adding the signatures would increase the download size significantly (it's ~5TiB of data for a specific _k_-size, ~15TiB for all three).

But the signatures are available and can be individually downloaded from [wort](https://wort.sourmash.bio)
:::

For this example we will use `k=21,s=100,000` to bring up a new local instance of branchwater.

## Cloning the repo

```bash
git clone https://github.com/sourmash-bio/branchwater
cd branchwater
```

## Create a new directory to hold the index and metadata

Let's create a new directory to hold the data for this service:

```bash
mkdir -p bw_k21
```

By the point we are ready to start the service it will look like this:
```
bw_k21
├── bqKey.json        # Only if building metadata yourself
├── index/            # branchwater index
├── metadata.parquet  # metadata for index, either prepared or built from index
└── sraids            # Only if building metadata yourself
```

## Edit `docker-compose.yml`

In the `volumes` section for the `index` and `mongodb` services,
replace `bw_db` with `bw_k21`:
```diff
     volumes:
-      - ./bw_db:/data/
+      - ./bw_k21:/data/
```

And in the `index` service, add the following lines to pass new parameters to the command that initializes the service:
```diff
+    command: >
+      /app/bin/branchwater-server
+        --port 80
+        -k 21
+        --scaled 100000
+        --location /dev/null
+        /data/index
```

:::{note}
Since we don't have the signatures,
we point `--location` to `/dev/null`.
Weird, but it works =]
:::

## Download the `k=21` index

Let's start by downloading the index. Here is a `wget` invocation to save it into `index/`:

```bash
pixi exec wget \
    -c --recursive \
    --no-parent -nH \
    --cut-dirs=3 --reject "index.html*" \
    -P bw_k21/index/ \
    https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-k21-s100000/
```

## Prepared metadata for index (or build your own!)

::::{tab-set}

:::{tab-item} Use prepared metadata

The metadata for these indices is already available at
<https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-metadata.parquet>
so you don't need to build it locally.
You can download it and put in the correct place with

```bash
pixi exec wget -c -O bw_k21/index/metadata.parquet \
    https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-metadata.parquet
```
:::

:::{tab-item} Build your own metadata

### Extract accessions from index

`sraids` is a list of all the SRA accessions used to build the index,
and we need it to retrieve the SRA metadata that is presented in the frontend.
This information is contained in the manifest used to build the index,
so we can extract it from the index and manifest by running

```bash
cargo run --release -p branchwater-index metadata bw_k21/index --acc-only -o bw_k21/sraids
```

### Edit `pyproject.toml`

There is one mention to `bw_db` in `pyproject.toml` that we need to change to
`bw_k21`, it is in the `[tool.pixi.feature.metadata.tasks]` section,
for the `metadata_bq` task:

```diff
-metadata_bq = { cmd = ["python3", "prepare_bq.py", "-a", "../bw_db/sraids", "-k", "../bw_db/bqKey.json", "-o", "../bw_db/metadata.parquet"], cwd = "metadata" }
+metadata_bq = { cmd = ["python3", "prepare_bq.py", "-a", "../bw_k21/sraids", "-k", "../bw_k21/bqKey.json", "-o", "../bw_k21/metadata.parquet"], cwd = "metadata" }
```

### BigQuery credentials

If you did the demo deployment you can copy and reuse it:
```
cp ../bw_db/bqKey.json .
```
Otherwise, follow [these instructions](deploy.md#prepare-a-bigquery-access-key) to create the BigQuery credential file.

### Build metadata

The final file we need is `metadata.parquet`,
and we have all the pieces in place to generate it.
Run
```bash
pixi run metadata_bq
```
to create it.

:::

::::

## Load metadata into mongodb

We can load `metadata.parquet` into mongodb by running
```bash
pixi run load_mongo
```

This will be printed after the command finishes:
```bash
1160375 acc documents imported to mongoDB collection
Full MongoDB size is 2304478866 bytes, average document size is 1985 bytes
```

:::{note}
Did you notice that 1,160,375 != 1,161,119? What is up with the missing metadata?

There is a longer discussion in <https://github.com/sourmash-bio/branchwater/issues/24#issuecomment-2067814713>
but it is mostly because there are metadata changes and datasets that were in previous versions
of branchwater might not have updated metadata anymore (due to retractions),
and we are downloading the most up-to-date metadata to serve.
We avoid removing the datasets from the search index to keep maintenance easier,
but they won't show up in the frontend without the metadata.

It is left as an exercise to the reader to figure out how to retrieve the ghost matches =]
:::

## Bring up the search index and frontend

Finally, we can bring up the index and frontend app:
```
pixi run deploy up -d
```

The website is now available at <http://localhost:8000>
