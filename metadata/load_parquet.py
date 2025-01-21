import datetime
import os
import re
import time

import polars as pl
import pymongo as pm


def main(*,
    metadata="/data/bw_db/metadata.parquet"):

    query_job = pl.read_parquet(metadata)

    meta_dic = []
    for row in query_job.iter_rows(named=True):
        meta_dic.append(dict(row.items()))

    # iterate over each dictionary in the list
    for d in meta_dic:
        # replace 'none' with NP
        for key in d:
            if type(d[key]) == list and len(d[key]) == 0:
                d[key] = 'NP'
            elif d[key] == None:
                d[key] = 'NP'

        # add biosample link
        d['biosample_link'] = f"https://www.ncbi.nlm.nih.gov/biosample/{d.get('biosample', '')}"

        # replace lat-lon with decimal degrees
        if 'lat_lon' in d and d['lat_lon'] != 'NP':
            regex = r'"(\d+\.\d+) ([NS]) (\d+\.\d+) ([EW])"'
            # extract latitude and longitude using regular expression
            match = re.search(regex, d['lat_lon'])
            if match:
                # convert latitude and longitude to decimal degrees
                lat = float(match.group(1))
                if match.group(2) == 'S':
                    lat *= -1
                lon = float(match.group(3))
                if match.group(4) == 'W':
                    lon *= -1
                # replace 'lat_lon' value with list of latitude and longitude
                d['lat_lon'] = [lat, lon]

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


    print(f'{sradb_col.count_documents({})} acc documents imported to mongoDB collection')

    # Retrieve statistics about the sradb_list collection
    stats = db.command("collstats", "sradb_list")

    # Extract the total size and average document size from the stats dictionary
    total_size = stats["size"]
    avg_doc_size = stats["avgObjSize"]

    print(
        f"Full MongoDB size is {total_size} bytes, average document size is {avg_doc_size} bytes")

    # print(sradb_col.find_one({}))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", default="/data/bw_db/metadata.parquet")

    args = parser.parse_args()
    main(metadata=args.metadata)
