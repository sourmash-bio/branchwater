# Deploying the SRA metagenomes index

The [deployment for the demo database](deploy.md) is useful when a
new search index is built from zero,
but in case you want to use an existing branchwater database there is
a more direct way that skips the `wort` signature download and indexing into a branchwater database.



In the case of the SRA metagenomes database from the [main instance](https://branchwater.sourmash.bio)
it is ~1.3 TiB as of 2024-11-28 for `s=1000`,
but we provide downscaled versions to `s=100,000` for `k={21,31,51}` containing the same `1,161,119` datasets that are easier to download and run locally:

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

```
git clone https://github.com/sourmash-bio/branchwater
cd branchwater
```

## Create a new directory to hold the index and metadata

```
mkdir -p bw_k21
cd bw_k21
```

## Download the `k=21` index

```
pixi exec wget -c --recursive --no-parent -nH --cut-dirs=3 --reject "index.html*" https://farm.cse.ucdavis.edu/~irber/branchwater/20241128-k21-s100000/ -P index/
```

## Extract manifest from index

```
cargo run --release -p branchwater-index metadata index -o manifest
tail -n +3 manifest|cut -d, -f1 | cut -d/ -f2|cut -d. -f1 > sraids
```

## Edit `docker-compose.yml`



## Prepare and load metadata

```
cp ../bw_db/bqKey.json .
pixi run metadata_bq
pixi run load_mongo
```

## Bring up the search index and frontend

```
pixi run deploy up -d
```

The website is now available at <http://localhost:8000>


