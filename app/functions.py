import pandas as pd
import io
import os
import gzip
import string
import markdown


DEFAULT_COLUMNS = ["SRA_accession", "containment", "cANI"]


class SearchError(Exception):
    """Search index errors"""


def getmetadata(config, http):
    # GET metadata stats from index server
    base_url = config.get('index_server', 'https://branchwater-api.jgi.doe.gov')
    r = http.request('GET', f"{base_url}/metadata/stats")
    if r.status != 200:
        raise SearchError(r.data.decode('utf-8'), r.status)

    metadata = r.json()

    return metadata


def getacc(signatures, config, http):
    # remove whitespace from string and compress signatures to gzipped bytes
    sig_str = signatures.translate({ord(c): None for c in string.whitespace})
    json_bytes = f"[{sig_str}]".encode('utf-8')
    buf = io.BytesIO()
    with gzip.open(buf, 'w') as fout:
        fout.write(json_bytes)

    # POST to mastiff
    base_url = config.get('index_server', 'https://branchwater-api.jgi.doe.gov')
    r = http.request('POST',
                     f"{base_url}/search",
                     body=buf.getvalue(),
                     headers={'Content-Type': 'application/json'})
    if r.status != 200:
        raise SearchError(r.data.decode('utf-8'), r.status)

    query_results_text = r.data.decode('utf-8')

    results_wrap_fp = io.StringIO(query_results_text)
    mastiff0_df = pd.read_csv(results_wrap_fp)
    n_raw_results = len(mastiff0_df)

    if n_raw_results == 0:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

    # containment to ANI
    ksize = config.get('ksize', 21)
    mastiff0_df['cANI'] = mastiff0_df['containment'] ** (1./ksize)

    # filter for containment; potential to pass this from user
    threshold = config.get('threshold', 0.1)
    print(
        f"Search returned {n_raw_results} results. Now filtering results with <{threshold} containment...")
    mastiff_df = mastiff0_df[mastiff0_df['containment'] >= threshold]
    print(
        f"Returning {len(mastiff_df)} filtered results!")

    # remove spaces from columns
    mastiff_df.columns = [c.replace(' ', '_') for c in mastiff_df.columns]
    return mastiff_df


def getmongo(acc_t, meta_list, config, client):
    db = client["sradb"]
    sradb_col = db["sradb_list"]

    # deselect ID; return acc and biosample html for every query
    meta_dict = {'_id': 0, 'acc': 1, 'biosample_link': 1}
    for item in meta_list:
        meta_dict[item] = 1

    query = list(sradb_col.find(
        {'acc': {"$in": acc_t}}, meta_dict))

    return (query)


def markdownify(md):
    return markdown.markdown(md)

