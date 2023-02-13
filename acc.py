import pandas as pd
import os
import sourmash
import screed
import io
import urllib3


def getacc(QUERY_SEQUENCE_FILE):
    run_info = pd.read_csv('sra.runinfo.csv.gz')

    # here replace with EBI?
    total_bp = 0
    sketch = sourmash.MinHash(0, 21, scaled=1000)
    with screed.open(QUERY_SEQUENCE_FILE) as records:
        for record in records:
            sketch.add_sequence(record.sequence, force=True)
            total_bp += len(record.sequence)

    ss = sourmash.SourmashSignature(sketch)
    buf = io.BytesIO()
    sourmash.save_signatures([ss], buf, compression=True)

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

    acc_t = tuple(mastiff_df.SRA_accession.tolist())
    return acc_t
