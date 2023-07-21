
import pandas as pd
import pymongo as pm
import time
import re
import datetime
import os
import yaml

from google.oauth2 import service_account
from google.cloud import bigquery

# get current directory
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f'dir_path: {dir_path}')
print(os.listdir(dir_path))

# get key and config paths
config_path = os.path.join(dir_path, 'config.yml')
key_path = os.path.join(dir_path, 'bqKey.json')

# use big query key
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
project_id = config.get('project_id', 'sraproject-386813')


# Connect to client
# bq key to service account with the roles: BigQuery Job User; BigQuery Data Owner; BigQuery Read Sessions User
credentials = service_account.Credentials.from_service_account_file(
    key_path)
client = bigquery.Client(credentials=credentials, project=project_id)
table_id = f'{project_id}.mastiffdata.mastiff_id'

# Create table of Mastiff accessions
# Not neccessary if up to date with metadata_prep/metacounts.py first
# ideally pulling from metadata-endpoint of mastiff API
runinfo = pd.read_csv(os.path.join(dir_path, 'sra.runinfo.csv'))
mastiff_acc = tuple(runinfo.Run.tolist())
client.delete_table(table_id, not_found_ok=True)  # delete table in case exists
df = pd.DataFrame(mastiff_acc, columns=['accID'])
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("accID", "STRING")])
client.load_table_from_dataframe(df, table_id, job_config=job_config)
time.sleep(30)  # potentially better as a a "while" loop
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
    attr_col = attr_col + \
        f'''json_query(jattr,'$.{item}_sam') as {item}, '''

for item in attr_list_nosam:
    attr_col = attr_col + \
        f'''json_query(jattr,'$.{item}') as {item}, '''

if config.get('build_full_db', False) == True:
    print(f'building full mongodb database.')
    limit = ";"
else:
    print(f'limiting mongodb to 150,000 for testing.')
    ## set LIMIT of 150,000 for testing (faster build) ##
    limit = "LIMIT 150000;"

query = f""" SELECT {column_col}, {attr_col} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `{table_id}` as mastacc ON metadata.acc = mastacc.accID {limit} """
print(f'query: {query}')

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
