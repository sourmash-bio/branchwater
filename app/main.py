from flask import Flask, render_template, request, jsonify, Response
import pandas as pd

from functions import *
import sys

app = Flask(__name__)  # create flask/app instance
app.config['SECRET_KEY'] = 'gibberish'  # may not be needed/not yet integrated
app.config['UPLOAD_FOLDER'] = 'static/files'  # may not be needed?


# define '/' and 'home' route
@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        # get signatures from fetch/promise API clientside
        form_data = request.get_json()
        print(f"Form JSON is {sys.getsizeof(form_data)} bytes.")

        # get acc from mastiff (imported from acc.py)
        signatures = form_data['signatures']
        mastiff_df = getacc(signatures)
        acc_t = tuple(mastiff_df.SRA_accession.tolist())

        # get metadata from mongodb (imported from mongoquery.py)
        meta_dic = form_data['metadata']
        meta_list = tuple([
                          key for key, value in meta_dic.items() if value])

        result_list = getmongo(acc_t, meta_list)
        print(f"Metadata for {len(result_list)} acc returned.")
        mastiff_dict = mastiff_df.to_dict('records')

        # Placeholder ANI calculation based on simple regression from csv at Phylum level
        # https://github.com/sourmash-bio/sourmash/issues/1859
        for r in result_list:
            for m in mastiff_dict:
                if r['acc'] == m['SRA_accession']:
                    r['containment'] = round(m['containment'], 2)
                    r['ANI_est'] = round(0.9984*m['containment']**0.0456, 2)
                    break

        return jsonify(result_list)  # return metadata results to client
    return render_template('index.html')


@app.route('/about', methods=['GET', "POST"])
def metadata():
    return render_template('about.html')


@app.route('/examples', methods=['GET', "POST"])
def examples():
    return render_template('examples.html')


if __name__ == '__main__':
    app.run(debug=True)
