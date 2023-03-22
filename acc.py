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

    # filter for containment; potential to pass this from user
    THRESHOLD = 0.2
    mastiff_df = mastiff0_df[mastiff0_df['containment'] >= THRESHOLD]
    print(
        f"Filtered to {len(mastiff_df)} mastiff acc results!")

    # acc column to string to pass to big query
    mastiff_df.columns = [c.replace(' ', '_') for c in mastiff_df.columns]

    return mastiff_df
