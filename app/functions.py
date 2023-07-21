import pymongo as pm
import pandas as pd
import io
import urllib3
import gzip
import string


def getacc(signatures):
    # remove whitespace from string and compress signatures to gzipped bytes
    sig_str = signatures.translate({ord(c): None for c in string.whitespace})
    json_bytes = sig_str.encode('utf-8')
    buf = io.BytesIO()
    with gzip.open(buf, 'w') as fout:
        fout.write(json_bytes)

    # POST to mastiff
    http = urllib3.PoolManager()
    r = http.request('POST',
                     'https://mastiff.sourmash.bio/search',
                     body=buf.getvalue(),
                     headers={'Content-Type': 'application/json'})
    query_results_text = r.data.decode('utf-8')

    results_wrap_fp = io.StringIO(query_results_text)
    mastiff0_df = pd.read_csv(results_wrap_fp)
    n_raw_results = len(mastiff0_df)

    # containment to ANI
    KSIZE = 21
    mastiff0_df['cANI'] = mastiff0_df['containment'] ** (1./KSIZE)
    # filter for containment; potential to pass this from user
    THRESHOLD = 0.1
    print(
        f"Search returned {n_raw_results} results. Now filtering results with <{THRESHOLD} containment...")
    mastiff_df = mastiff0_df[mastiff0_df['containment'] >= THRESHOLD]
    print(
        f"Returning {len(mastiff_df)} filtered results!")
 

    # remove spaces from columns
    mastiff_df.columns = [c.replace(' ', '_') for c in mastiff_df.columns]
    return mastiff_df


def getmongo(acc_t, meta_list):
    # connection to run locally
    # client = pm.MongoClient("mongodb://localhost:27017/")

    # connection for docker container
    repo_name = 'branchwater-web'
    client = pm.MongoClient(f"mongodb://{repo_name}-mongo-readonly-1")
    db = client["sradb"]
    sradb_col = db["sradb_list"]

    # deselect ID; return acc and biosample html for every query
    meta_dict = {'_id': 0, 'acc': 1, 'biosample_link': 1}
    for item in meta_list:
        meta_dict[item] = 1

    query = list(sradb_col.find(
        {'acc': {"$in": acc_t}}, meta_dict))

    return (query)
