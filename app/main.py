import os
import yaml
from flask import Flask, render_template, request, jsonify
from functions import *

import sentry_sdk
from sentry_sdk.integrations.pymongo import PyMongoIntegration
sentry_sdk.init(
    os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[
        PyMongoIntegration(),
    ],
)

app = Flask(__name__)  # create flask/app instance
# may not be needed/not yet integrated
#app.config['SECRET_KEY'] = 'my-secret-key'

# add markdownify filter to jinja2 (imported from functions.py)
app.jinja_env.filters['markdownify'] = markdownify

# Load configuration from config.yaml
with open('config.yml', 'r') as file:
    config_data = yaml.safe_load(file)

    app.config.update(config_data)


KSIZE = app.config.get('ksize', 21)
THRESHOLD = app.config.get('threshold', 0.1)
print(f'ksize: {KSIZE}')
print(f'threshold: {THRESHOLD}')

# define '/' and 'home' route

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        # get signatures from fetch/promise API clientside
        form_data = request.get_json()

        # get acc from mastiff (imported from acc.py)
        signatures = form_data['signatures']
        try:
            mastiff_df = getacc(signatures, app.config)
        except SearchError as e:
            return e.args

        acc_t = tuple(mastiff_df.SRA_accession.tolist())

        # for 'basic' query, override metadata form with selected categories
        meta_list = ('bioproject', 'assay_type',
                     'collection_date_sam', 'geo_loc_name_country_calc', 'organism', 'lat_lon')

        # get metadata from mongodb (imported from mongoquery.py)
        result_list = getmongo(acc_t, meta_list, app.config)
        print(f"Metadata for {len(result_list)} acc returned.")
        mastiff_dict = mastiff_df.to_dict('records')

        for r in result_list:
            for m in mastiff_dict:
                if r['acc'] == m['SRA_accession']:
                    r['containment'] = round(m['containment'], 2)
                    r['cANI'] = round(m['cANI'], 2)
                    break

        return jsonify(result_list)  # return metadata results to client
    return render_template('index.html')


@app.route('/advanced', methods=['GET', "POST"])
def advanced():
    if request.method == 'POST':
        # get signatures from fetch/promise API clientside
        form_data = request.get_json()
        # print(f"Form JSON is {sys.getsizeof(form_data)} bytes.")

        # get acc from mastiff (imported from acc.py)
        signatures = form_data['signatures']
        try:
            mastiff_df = getacc(signatures, app.config)
        except SearchError as e:
            return e.args

        acc_t = tuple(mastiff_df.SRA_accession.tolist())

        # get metadata from mongodb (imported from mongoquery.py)
        meta_dic = form_data['metadata']
        meta_list = tuple([
                          key for key, value in meta_dic.items() if value])

        result_list = getmongo(acc_t, meta_list, app.config)
        print(f"Metadata for {len(result_list)} acc returned.")
        mastiff_dict = mastiff_df.to_dict('records')

        for r in result_list:
            for m in mastiff_dict:
                if r['acc'] == m['SRA_accession']:
                    r['containment'] = round(m['containment'], 2)
                    r['cANI'] = round(m['cANI'], 2)
                    break

        return jsonify(result_list)  # return metadata results to client
    return render_template('advanced.html')


@app.route('/about', methods=['GET', "POST"])
def metadata():
    return render_template('about.html')

@app.route('/test', methods=['GET', "POST"])
def testme():
    x = render_template("test.md")
    print(x)
    return x

@app.route('/contact', methods=['GET', "POST"])
def contact():
    return render_template('contact.html')

@app.route('/examples', methods=['GET', "POST"])
def examples():
    # note, fetch call sends to '/' route to return 'simple search' results
    return render_template('examples.html')


# in production this changes:
#
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
