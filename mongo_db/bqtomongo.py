
import pandas as pd
import pymongo as pm
import time
import re
import datetime

from google.oauth2 import service_account
from google.cloud import bigquery
from keypath import bq_path


# Connect to client
# bq key to service account with the roles: BigQuery Job User; BigQuery Data Owner; BigQuery Read Sessions User
credentials = service_account.Credentials.from_service_account_file(
    bq_path)
project_id = 'sraproject-384718'
client = bigquery.Client(credentials=credentials, project=project_id)
table_id = f'sraproject-384718.mastiffdata.mastiff_id'

# Create table of Mastiff accessions
# Not neccessary if up to date with metadata_prep/metacounts.py first
# ideally pulling from metadata-endpoint of mastiff API
runinfo = pd.read_csv('metadata_prep/sra.runinfo.csv')
mastiff_acc = tuple(runinfo.Run.tolist())
client.delete_table(table_id, not_found_ok=True)  # delete table in case exists
df = pd.DataFrame(mastiff_acc, columns=['accID'])
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("accID", "STRING")])
client.load_table_from_dataframe(df, table_id, job_config=job_config)
time.sleep(30)  # potentially better as a a "while" loop
destination_table = client.get_table(table_id)
print("Loaded {} mastiff accs.".format(destination_table.num_rows))


# import the table of attributes and counts at >4.5%
filt_df = pd.read_csv('metadata_prep/attrcounts_4.5percent.csv')

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
    attr_col = attr_col + \
        f'''json_query(jattr,'$.{item}_sam') as {item}, '''

for item in attr_list_nosam:
    attr_col = attr_col + \
        f'''json_query(jattr,'$.{item}') as {item}, '''

## note LIMIT for initial build #
query = f""" SELECT {column_col}, {attr_col} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `{table_id}` as mastacc ON metadata.acc = mastacc.accID LIMIT 140000; """

query_job = client.query(query)
time.sleep(30)  # potentially better as a a "while" loop
meta_dic = []
for row in query_job:
    meta_dic.append(dict(row.items()))

meta_dic_cp = meta_dic  # make copy for troubleshooting


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


for d in meta_dic:
    for key, value in d.items():
        if isinstance(value, datetime.date):
            d[key] = str(value)


# connect to mongodb client, clear collection, and insert
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["sradb"]
sradb_col = db["sradb_list"]
sradb_col.drop()  # delete current collection
res = sradb_col.insert_many(meta_dic)


# update mongodb with biosample link
# needs to be added sooner

# Loop through each document in the collection
# SLOW - do prior to document insertion in the final build
for document in sradb_col.find():
    biosample_value = document['biosample']
    biosample_link_value = 'https://www.ncbi.nlm.nih.gov/biosample/{}'.format(
        biosample_value)
    document['biosample_link'] = biosample_link_value
    sradb_col.replace_one({'_id': document['_id']}, document)


print(f'{sradb_col.count_documents({})} acc documents imported to mongoDB collection')


print(sradb_col.find_one({}))
print(db.command("collstats", "sradb_list"))
