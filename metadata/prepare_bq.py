import datetime
import re
import os
import time
from pathlib import Path

import pandas as pd
import polars as pl
import yaml

from google.oauth2 import service_account
from google.cloud import bigquery

def main(
    *,
    accs="/data/bw_db/sraids",
    sra_metadata="s3://sra-pub-metadata-us-east-1/sra/metadata/",
    build_full_db=True,
    output="/data/bw_db/metadata.parquet",
    key_path="/data/bw_db/bqKey.json",
    project_id='sraproject-386813',
):
    # get current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f'dir_path: {dir_path}')
    print(os.listdir(dir_path))

    # Connect to client
    # bq key to service account with the roles: BigQuery Job User; BigQuery Data Owner; BigQuery Read Sessions User
    credentials = service_account.Credentials.from_service_account_file(
        key_path)
    client = bigquery.Client(credentials=credentials, project=project_id)
    table_id = f'{project_id}.mastiffdata.mastiff_id'

    # Create table of Mastiff accessions
    # Not neccessary if up to date with metadata_prep/metacounts.py first
    # ideally pulling from metadata-endpoint of mastiff API
    mastiff_acc = Path(accs).read_text().splitlines()
    client.delete_table(table_id, not_found_ok=True)  # delete table in case exists
    df = pd.DataFrame(mastiff_acc, columns=['accID'])
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("accID", "STRING")])
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    destination_table = client.get_table(table_id)
    print("Loaded {} mastiff accs to a bq table.".format(destination_table.num_rows))


    # import the table of attributes and counts at >4.5%
    # csv copied from outputs of metadata_prep
    filt_df = pd.read_csv(os.path.join(dir_path, 'attrcounts_4.5percent.csv'))

    # Create bq query to flatten table
    # Tuple of attr located in columns in bq
    column_list = tuple(filt_df.loc[filt_df['in_jattr'] != 1, 'HarmonizedName'])
    # Tuble of attr located in jattr without '_sam' suffix
    attr_list_nosam = tuple(filt_df.loc[(filt_df['in_jattr'] == 1) & (
        filt_df['not_sam'] == 1), 'HarmonizedName'])
    # Tuble of attr located in jattr with '_sam' suffix
    attr_list_sam = tuple(filt_df.loc[(filt_df['in_jattr'] == 1) & (
        filt_df['not_sam'] != 1), 'HarmonizedName'])


    # Create bigQuery string for each query type
    column_col = ''
    for item in column_list:
        column_col = column_col + \
            f'''{item}, '''

    column_col = column_col[:-2]

    attr_col = ''
    for item in attr_list_sam:
        attrib = f'''json_query(jattr,'$.{item}_sam') as {item}, '''
        if 'lat_lon' in item:
            attrib = f'''json_query(jattr,'$.{item}_sam_s_dpl34') as {item}, '''

        attr_col = attr_col + attrib

    for item in attr_list_nosam:
        attr_col = attr_col + \
            f'''json_query(jattr,'$.{item}') as {item}, '''

    if build_full_db == True:
        print(f'building full mongodb database.')
        limit = ";"
    else:
        print(f'limiting mongodb to 150,000 for testing.')
        ## set LIMIT of 150,000 for testing (faster build) ##
        limit = "LIMIT 150000;"

    query = f""" SELECT {column_col}, {attr_col} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `{table_id}` as mastacc ON metadata.acc = mastacc.accID {limit} """
    print(f'query: {query}')

    query_job = client.query(query)

    rows = query_job.result()  # Waits for query to finish
    df = pl.from_arrow(rows.to_arrow())

    # write df to parquet
    df.write_parquet(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--acc", default="/data/bw_db/sraids")
    parser.add_argument(
        "-s", "--sra-metadata", default="s3://sra-pub-metadata-us-east-1/sra/metadata/"
    )
    parser.add_argument("-o", "--output", default="/data/bw_db/metadata.parquet")
    parser.add_argument("-k", "--key-path", default="/data/bw_db/bqKey.json")
    parser.add_argument("-p", "--project-id", default='sraproject-386813')

    args = parser.parse_args()
    main(accs=args.acc, sra_metadata=args.sra_metadata, output=args.output,
         key_path=args.key_path, project_id=args.project_id)
