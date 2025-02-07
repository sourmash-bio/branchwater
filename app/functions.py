import polars as pl
import io
import os
import gzip
import string


DEFAULT_COLUMNS = {
    "SRA_accession": pl.String,
    "containment": pl.Float64,
    "cANI": pl.Float64
}


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
    mastiff_df = pl.read_csv(results_wrap_fp, schema=DEFAULT_COLUMNS)
    n_raw_results = len(mastiff_df)

    if n_raw_results == 0:
        return pl.DataFrame(None, schema=DEFAULT_COLUMNS)

    ksize = int(config.metadata['ksize'])

    threshold = config.get('threshold', 0.1)
    print(
        f"Search returned {n_raw_results} results. Now filtering results with <{threshold} containment...")

    mastiff_df = (mastiff_df
        # filter for containment; potential to pass this from user
        .filter(pl.col("containment") >= threshold)
        .with_columns(
          # containment to ANI
          cANI=pl.col('containment') ** (1./ksize)
        ))

    print(
        f"Returning {len(mastiff_df)} filtered results!")

    # remove spaces from columns
    mastiff_df = mastiff_df.rename(lambda c: c.replace(' ', '_'))
    return mastiff_df


def getduckdb(mastiff_df, meta_list, config, client):
    required = ["acc"]
    # make sure required keys are present, and show up first
    meta_list = list(dict.fromkeys(required + list(meta_list)))

    query = f"""
        SELECT
            subset.acc,
            round(accs.containment, 2) as containment,
            round(accs.cANI, 2) as cANI,
            subset.* EXCLUDE (acc)
        FROM mastiff_df accs
        LEFT JOIN (SELECT {", ".join(meta_list)} FROM metadata) subset
        ON accs.SRA_accession = subset.acc;
    """
    result = client.sql(query)

    return result
