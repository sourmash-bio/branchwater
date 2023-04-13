import pandas as pd
import time
import datetime
import dateutil.parser


from google.oauth2 import service_account
from google.cloud import bigquery
from keypath import bq_path

import pymongo as pm


# Need to add language to replace 'null' to a different value


# mastiff acc list - update to pull from mastiff API
runinfo = pd.read_csv('sra.runinfo.csv')
mastiff_acc = tuple(runinfo.Run.tolist())


# JATTR of attr in >5% of samp
jattr_list = ('run_file_create_date', 'bases', 'lat_lon_sam', 'env_biome_sam', 'env_feature_sam', 'host_sam', 'env_material_sam', 'sample_type_sam',
              'depth_sam', 'isolate_sam', 'age_sam', 'env_broad_scale_sam', 'env_medium_sam', 'env_local_scale_sam', 'altitude_sam', 'source_material_id_sam')
jattr_str = ''
for item in jattr_list:
    jattr_str = jattr_str + f'''json_query(jattr,'$.{item}') as {item}, '''

jattr_str = jattr_str[:-2]


# string of metadata
meta_list = f"acc, assay_type, experiment, librarysource, organism, geo_loc_name_country_calc, collection_date_sam, geo_loc_name_country_continent_calc, geo_loc_name_sam, {jattr_str}"

# bq table parameters
credentials = service_account.Credentials.from_service_account_file(
    bq_path)
project_id = 'sraquery-375913'
client = bigquery.Client(credentials=credentials, project=project_id)
# add {datetime.date.today()} to table id when final
table_id = f'sraquery-375913.testdataset.mastiff_id'


# upload acc to bq table
client.delete_table(table_id, not_found_ok=True)  # delete table in case exists

df = pd.DataFrame(mastiff_acc, columns=['accID'])
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("accID", "STRING")])
client.load_table_from_dataframe(df, table_id, job_config=job_config)
time.sleep(30)  # possibly best as a "while" loop
destination_table = client.get_table(table_id)
print("Loaded {} mastiff accs.".format(destination_table.num_rows))

# query and save to dictionary
# note limit out records output
query = f""" SELECT {meta_list} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `{table_id}` as mastacc ON metadata.acc = mastacc.accID LIMIT 140000; """
query_job = client.query(query)
meta_dic = []
for row in query_job:
    meta_dic.append(dict(row.items()))

meta_dic_cp = meta_dic
# here replace datatypes that cause errors in mongodb

for item in meta_dic:
    if 'run_file_create_date' in item:
        # convert the value to a string and remove any extra quotes
        date_string = str(item['run_file_create_date']).strip('"')
        try:
            parsed_date = dateutil.parser.parse(
                date_string).strftime('%Y-%m-%d %H:%M:%S')
            item['run_file_create_date'] = parsed_date
        except ValueError:
            pass  #

# replace empty or None's with 'NP'
for item in meta_dic:
    for key in item:
        if type(item[key]) == list and len(item[key]) == 0:
            item[key] = 'NP'
        elif item[key] == None:
            item[key] = 'NP'


# remove any more errors that could occur from improper date-time formatting
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
print(f'{sradb_col.count_documents({})} acc documents imported to mongoDB collection')


print(db.command("collstats", "sradb_list"))

print(sradb_col.find_one({}))
