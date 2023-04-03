from flask import Flask, render_template, request, jsonify, Response
import pandas as pd

from acc import *
from mongoquery import *
import json
import sys
# import random
import plotly
import plotly.express as px


app = Flask(__name__)  # create flask/app instance
app.config['SECRET_KEY'] = 'gibberish'
app.config['UPLOAD_FOLDER'] = 'static/files'


def generate_json_chunks(data):
    chunk_size = 100  # number of items to send in each chunk
    num_chunks = len(data) // chunk_size + 1
    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = min(start_index + chunk_size, len(data))
        chunk_data = data[start_index:end_index]
        chunk_json = json.dumps({'data': chunk_data})
        yield f"data: {chunk_json}\n\n"


# add ability to access html templates for form with form = +return
# decorator to tell what URL triggers function
@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        form_data = request.get_json()
        print(f"JSON is {sys.getsizeof(form_data)} bytes!")
        print(form_data)

        # get acc from imported functions
        signatures = form_data['signatures']
        mastiff_df = getacc(signatures)
        acc_t = tuple(mastiff_df.SRA_accession.tolist())

        # get metadata from imported function
        meta_dic = form_data['metadata']
        meta_list = tuple([key for key, value in meta_dic.items() if value])
        result_list = getmongo(acc_t, meta_list)
        print(f"Metadata for {len(result_list)} acc returned!")
        mastiff_dict = mastiff_df.to_dict('records')

        # Placeholder ANI calculation based on simple regression from csv at Phylum level
        # https://github.com/sourmash-bio/sourmash/issues/1859
        for r in result_list:
            for m in mastiff_dict:
                if r['acc'] == m['SRA_accession']:
                    r['containment'] = m['containment']
                    r['ANI_est'] = 0.9984*m['containment']**0.0456
                    break
        print(result_list)

        return jsonify(result_list)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
