import os
import pandas as pd
import db_dtypes
import time
import random

from google.oauth2 import service_account
import googleapiclient.discovery

from google.cloud import bigquery
from google.oauth2 import service_account
from keypath import bq_path


testacc_t = ('SRR18036904', 'SRR18036905', 'SRR18036906',
             'SRR18036904', 'SRR18036905', 'SRR18036906')

# basic for now; can be updated with user inputs
meta_list = f"acc, organism"

# Option 1 - populates table with acc, then joins table, then clears table (temp table not allowed with big query?)


def getmeta(acc_t, meta_list):
    # construct Big Query client object
    # note: has LIMIT 300 while in development
    credentials = service_account.Credentials.from_service_account_file(
        bq_path)
    project_id = 'sraquery-375913'
    client = bigquery.Client(credentials=credentials, project=project_id)
    s1 = "'),('"
    query = f"""DELETE FROM sraquery-375913.testdataset.accs WHERE true; INSERT INTO `sraquery-375913.testdataset.accs` (accID) VALUES('{s1.join(acc_t)}'); SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `sraquery-375913.testdataset.accs` as acctest ON metadata.acc = acctest.accID LIMIT 3000; """
    return client.query(query).to_dataframe()


# option 2: supposedley less efficient
def getmeta2(acc_t, meta_list):
    # construct Big Query client object
    # note: has LIMIT 300 while in development
    credentials = service_account.Credentials.from_service_account_file(
        bq_path)
    project_id = 'sraquery-375913'
    client = bigquery.Client(credentials=credentials, project=project_id)
    s2 = "','"
    query2 = f"""SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` WHERE acc in ('{s2.join(acc_t)}') limit 100000;"""
    return client.query(query2).to_dataframe()


# option 3 dataframe-join
def getmeta3(acc_t, meta_list):
    # setup bq parameters
    credentials = service_account.Credentials.from_service_account_file(
        bq_path)
    project_id = 'sraquery-375913'
    client = bigquery.Client(credentials=credentials, project=project_id)
    table_num = random.randint(1000, 9999)
    table_id = f'sraquery-375913.testdataset.{table_num}'

    # upload acc to bq
    df = pd.DataFrame(acc_t, columns=['accID'])
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("accID", "STRING")])
    client.load_table_from_dataframe(df, table_id, job_config=job_config)
    time.sleep(2)  # possibly best as a "while" loop
    destination_table = client.get_table(table_id)
    print("Loaded {} accs.".format(destination_table.num_rows))

    # query and save to df
    query = f"""SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `{table_id}` as acctest ON metadata.acc = acctest.accID LIMIT 3000; """
    meta_df = client.query(query).to_dataframe()
    client.delete_table(table_id, not_found_ok=True)  # delete table
    print("Deleted table '{}'.".format(table_id))
    return meta_df


# option 4, testing time for in-line query, potentially as a loop
def getmeta4(acc_t, meta_list):
    # construct Big Query client object
    # note: has LIMIT 300 while in development
    credentials = service_account.Credentials.from_service_account_file(
        bq_path)
    project_id = 'sraquery-375913'
    client = bigquery.Client(credentials=credentials, project=project_id)
    s2 = "','"

    acc1 = (acc_t[0:50000])
    acc2 = (acc_t[50001:len(acc_t)])

    query1 = f"""SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` WHERE acc in ('{s2.join(acc1)}') limit 100000;"""
    df1 = client.query(query1).to_dataframe()
    query2 = f"""SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` WHERE acc in ('{s2.join(acc2)}') limit 100000;"""
    df2 = client.query(query2).to_dataframe()

    df = pd.concat(df1, df2)

    return df
