import os
import pandas as pd
import db_dtypes

from google.oauth2 import service_account
import googleapiclient.discovery

from google.cloud import bigquery
from google.oauth2 import service_account
from keypath import bq_path


testacc_t = ('SRR18036904', 'SRR18036905', 'SRR18036906')
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


# OPTION 2; supposed to take longer
#       credentials = service_account.Credentials.from_service_account_file(bq_path)
 #   project_id = 'sraquery-375913'
  #  client = bigquery.Client(credentials=credentials, project=project_id)
# s2 = "','"
# query2 = f"""SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` WHERE acc in ('{s2.join(acc_t)}') limit 100000;"""
# query_job = client.query(query2)
# client.query(query).result()
