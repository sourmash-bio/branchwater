import time
import re
import datetime
import os

import polars as pl
import pymongo as pm


def main(
    *,
    accs="/data/bw_db/sraids",
    sra_metadata="s3://sra-pub-metadata-us-east-1/sra/metadata/",
    build_full_db=True,
):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"dir_path: {dir_path}")
    print(os.listdir(dir_path))

    # Create table of Mastiff accessions
    # Not neccessary if up to date with metadata_prep/metacounts.py first
    # ideally pulling from metadata-endpoint of mastiff API
    mastiff_acc = pl.scan_csv(accs, has_header=False, new_columns=["acc"])

    print(f"Loaded {len(mastiff_acc.collect())} mastiff accs.")

    # import the table of attributes and counts at >4.5%
    # csv copied from outputs of metadata_prep
    filt_df = pl.read_csv(os.path.join(dir_path, "attrcounts_4.5percent.csv"))

    # Create bq query to flatten table
    # Tuple of attr located in columns in bq
    column_list = (
        filt_df.filter(pl.col("in_jattr").is_null())
        .get_column("HarmonizedName")
        .to_list()
    )
    # Tuple of attr located in jattr without '_sam' suffix
    attr_list_nosam = (
        filt_df.filter((pl.col("in_jattr") == 1) & (pl.col("not_sam") == 1))
        .get_column("HarmonizedName")
        .to_list()
    )
    # Tuple of attr located in jattr with '_sam' suffix
    attr_list_sam = (
        filt_df.filter((pl.col("in_jattr") == 1) & (pl.col("not_sam").is_null()))
        .get_column("HarmonizedName")
        .to_list()
    )

    print(
        pl.scan_parquet(
            sra_metadata,
            storage_options={"skip_signature": "true"},
        ).collect_schema()
    )

    sra_metadata = (
        pl.scan_parquet(
            sra_metadata,
            storage_options={"skip_signature": "true"},
        )
        .select(
            [pl.col(col) for col in column_list]
            + [
                (
                    pl.col("jattr").str.json_path_match(f"$.{item}_sam").alias(item)
                    if "lat_lon" not in item
                    else (
                        pl.col("jattr")
                        .str.json_path_match(f"$.{item}_sam_s_dpl34")
                        .alias(item)
                    )
                )
                for item in attr_list_sam
            ]
            + [
                pl.col("jattr").str.json_path_match(f"$.{item}").alias(item)
                for item in attr_list_nosam
            ]
        )
        .with_columns(lat_lon=pl.col("lat_lon").str.replace("", ""))
    )

    if build_full_db:
        print(f"building full mongodb database.")
    else:
        print(f"limiting mongodb to 150,000 for testing.")
        sra_metadata = sra_metadata.head(150000)

    print(sra_metadata.explain(optimized=True))

    query_job = sra_metadata.join(mastiff_acc, on="acc").sink_parquet("test.parquet")

    print(query_job)

    query_job = client.query(query)
    time.sleep(30)  # potentially better as a a "while" loop
    meta_dic = []
    for row in query_job:
        meta_dic.append(dict(row.items()))

    # iterate over each dictionary in the list
    for d in meta_dic:
        # replace 'none' with NP
        for key in d:
            if type(d[key]) == list and len(d[key]) == 0:
                d[key] = "NP"
            elif d[key] == None:
                d[key] = "NP"

        # add biosample link
        d["biosample_link"] = (
            f"https://www.ncbi.nlm.nih.gov/biosample/{d.get('biosample', '')}"
        )

        # replace lat-lon with decimal degrees
        if "lat_lon" in d and d["lat_lon"] != "NP":
            regex = r'"(\d+\.\d+) ([NS]) (\d+\.\d+) ([EW])"'
            # extract latitude and longitude using regular expression
            match = re.search(regex, d["lat_lon"])
            if match:
                # convert latitude and longitude to decimal degrees
                lat = float(match.group(1))
                if match.group(2) == "S":
                    lat *= -1
                lon = float(match.group(3))
                if match.group(4) == "W":
                    lon *= -1
                # replace 'lat_lon' value with list of latitude and longitude
                d["lat_lon"] = [lat, lon]

        # remove any more errors that could occur from improper date-time formatting by converting to string
        for key, value in d.items():
            if isinstance(value, datetime.date):
                d[key] = str(value)

    # connect to mongodb client, clear collection, and insert
    # For now default client settings, needs to be changed for app deployment with port
    # client = pm.MongoClient(, 27017)  # in first location insert the port
    client = pm.MongoClient("mongodb://localhost:27017/")
    db = client["sradb"]
    sradb_col = db["sradb_list"]
    sradb_col.drop()  # delete current collection if already present
    res = sradb_col.insert_many(meta_dic)

    print(
        f"{sradb_col.count_documents({})} acc documents imported to mongoDB collection"
    )

    # Retrieve statistics about the sradb_list collection
    stats = db.command("collstats", "sradb_list")

    # Extract the total size and average document size from the stats dictionary
    total_size = stats["size"]
    avg_doc_size = stats["avgObjSize"]

    print(
        f"Full MongoDB size is {total_size} bytes, average document size is {avg_doc_size} bytes"
    )

    # print(sradb_col.find_one({}))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--acc", default="/data/bw_db/sraids")
    parser.add_argument(
        "-s", "--sra-metadata", default="s3://sra-pub-metadata-us-east-1/sra/metadata/"
    )

    args = parser.parse_args()
    main(accs=args.acc, sra_metadata=args.sra_metadata)
