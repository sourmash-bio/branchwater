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

    # currently loads results to panda df
    # here change to .json

    results_wrap_fp = io.StringIO(query_results_text)
    mastiff0_df = pd.read_csv(results_wrap_fp)
    print(f"Loaded {len(mastiff0_df)} mastiff results into a dataframe!")

    # filter for containment
    THRESHOLD = 0.2
    mastiff_df = mastiff0_df[mastiff0_df['containment'] >= THRESHOLD]

    mastiff2_df = mastiff_df.set_index('SRA accession').join(
        run_info.set_index('Run')['ScientificName'])
    mastiff2_df.head()

    null_df = mastiff2_df[mastiff2_df['ScientificName'].isnull()]

    mastiff3_df = mastiff2_df[~mastiff2_df['ScientificName'].isnull()]

    print(f"Of {len(mastiff2_df)} MAGsearch results, {len(mastiff3_df)} have non-null ScientificName")
