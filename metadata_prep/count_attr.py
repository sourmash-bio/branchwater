import pandas as pd
import time


from google.oauth2 import service_account
from google.cloud import bigquery
from keypath import bq_path

# Create table of acc in mastiff
# mastiff acc list - update to pull from mastiff API
runinfo = pd.read_csv('prepscripts/sra.runinfo.csv')
mastiff_acc = tuple(runinfo.Run.tolist())

# bq key and table parameters
credentials = service_account.Credentials.from_service_account_file(
    bq_path)
project_id = 'sraproject-384718'
client = bigquery.Client(credentials=credentials, project=project_id)
table_id = f'sraproject-384718.mastiffdata.mastiff_id'

# upload mastiff acc to bq table
client.delete_table(table_id, not_found_ok=True)  # delete table in case exists
df = pd.DataFrame(mastiff_acc, columns=['accID'])
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("accID", "STRING")])
client.load_table_from_dataframe(df, table_id, job_config=job_config)
time.sleep(30)  # potentially better as a a "while" loop
destination_table = client.get_table(table_id)
print("Loaded {} mastiff accs.".format(destination_table.num_rows))


# Upload attribute list of ~1000 attributes
# Attributes compiled from big query, https://www.ncbi.nlm.nih.gov/biosample/docs/attributes/, and https://www.ncbi.nlm.nih.gov/sra/docs/sra-cloud-based-metadata-table/
df = pd.read_csv('prepscripts/attributeList.csv')

# Tuple of attr located in columns in bq
column_list = tuple(df.loc[df['in_jattr'] != 1, 'HarmonizedName'])
# Tuble of attr located in jattr without '_sam' suffix
attr_list_nosam = tuple(df.loc[(df['in_jattr'] == 1) & (
    df['not_sam'] == 1), 'HarmonizedName'])
# Tuble of attr located in jattr with '_sam' suffix
attr_list_sam = tuple(df.loc[(df['in_jattr'] == 1) & (
    df['not_sam'] != 1), 'HarmonizedName'])

print(
    f"Counts will be from {len(column_list)} columns and {len(attr_list_sam)+len(attr_list_nosam)} attributes.")

# Create bigQuery string for each query type
column_col = ''
for item in column_list:
    column_col = column_col + \
        f'''COUNT('{item}') as {item}, '''

column_col = column_col[:-2]

attr_col = ''
for item in attr_list_sam:
    attr_col = attr_col + \
        f'''COUNT(json_query(jattr,'$.{item}_sam')) as {item}, '''

for item in attr_list_nosam:
    attr_col = attr_col + \
        f'''COUNT(json_query(jattr,'$.{item}')) as {item}, '''

# col_list_all = f"{column_col}, {attr_col}"
query_all = f""" SELECT {column_col}, {attr_col} FROM `nih-sra-datastore.sra.metadata` as metadata INNER JOIN `{table_id}` as mastacc ON metadata.acc = mastacc.accID; """

# Convert query to df and table for CSV
results = client.query(query_all)
results_df = results.to_dataframe()
df_t = results_df.T.reset_index()
df_t.columns = ['HarmonizedName', 'counts']

# calculate percentages and add as new column
df_t['percentage'] = (df_t['counts'] / df_t['counts'].max())*100

# update attributeList with information and save
df_updated = pd.merge(df, df_t, on='HarmonizedName')

# filter for >4.5% provided
filt_df = df_t[df_t['percentage'] > 4.5]

print("{} attributes have data available for >4.5% of accessions.".format(len(filt_df)))
df_updated.to_csv("prepscripts/attrcounts.csv", index=False)
filt_df.to_csv("prepscripts/attrcounts_4.5percent.csv", index=False)
