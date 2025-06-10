import time
import re
import datetime
import os

import polars as pl


def main(
    *,
    accs="/data/bw_db/sraids",
    sra_metadata="s3://sra-pub-metadata-us-east-1/sra/metadata/",
    build_full_db=True,
    output="/data/bw_db/metadata.parquet",
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
            storage_options={"skip_signature": "true",
                             "aws_region": "us-east-1"},
        ).collect_schema()
    )

    sra_metadata = (
        pl.scan_parquet(
            sra_metadata,
            storage_options={"skip_signature": "true",
                             "aws_region": "us-east-1"},
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
        print(f"building full metadata database.")
    else:
        print(f"limiting metadata to 150,000 for testing.")
        sra_metadata = sra_metadata.head(150000)

    # print(sra_metadata.explain(optimized=True))

    query_job = sra_metadata.join(mastiff_acc, on="acc").sink_parquet(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--acc", default="/data/bw_db/sraids")
    parser.add_argument(
        "-s", "--sra-metadata", default="s3://sra-pub-metadata-us-east-1/sra/metadata/"
    )
    parser.add_argument("-o", "--output", default="/data/bw_db/metadata.parquet")
    parser.add_argument('--build-full-db', action="store_true", default=True)
    parser.add_argument('--build-test-db', dest="build_full_db", action="store_false")

    args = parser.parse_args()
    main(accs=args.acc, sra_metadata=args.sra_metadata, output=args.output, build_full_db=args.build_full_db)
