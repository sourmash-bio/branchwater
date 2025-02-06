import os

import duckdb
import yaml
import urllib3
from flask import Flask, render_template, request, jsonify, g, current_app

import sentry_sdk
sentry_sdk.init(
    os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

from functions import getacc, getmetadata, getduckdb, SearchError


def http_pool():
    if 'pool' not in g:
        g.pool = urllib3.PoolManager()

    return g.pool

def duckdb_client(config):
    if 'duckdb_client' not in g:
        g.duckdb_client = duckdb.connect(database = config['metadata_duckdb'],
                                         read_only=True)

    return g.duckdb_client

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # may not be needed/not yet integrated
        current_app.config['SECRET_KEY'] = 'my-secret-key'

        # Load configuration from config.yaml
        with open('config.yml', 'r') as file:
            config_data = yaml.safe_load(file)

            current_app.config.update(config_data)

            metadata = getmetadata(current_app.config, http_pool())
            current_app.config.metadata = metadata

    return app

app = create_app()  # create flask/app instance

@app.teardown_appcontext
def teardown_http_pool(exception):
    pool = g.pop('pool', None)

    if pool is not None:
        pool.clear()

@app.teardown_appcontext
def teardown_duckdb_client(exception):
    client = g.pop('duckdb_client', None)

    if client is not None:
        client.close()


KSIZE = app.config.get('ksize', 21)
THRESHOLD = app.config.get('threshold', 0.1)
METADATA = app.config.get('metadata', {})
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
            mastiff_df = getacc(signatures, app.config, http_pool())
        except SearchError as e:
            return e.args

        # for 'basic' query, override metadata form with selected categories
        meta_list = ('bioproject', 'assay_type',
                     'collection_date_sam', 'geo_loc_name_country_calc', 'organism', 'lat_lon')

        # get metadata from duckdb
        result_list = getduckdb(mastiff_df, meta_list, app.config, duckdb_client(app.config)).pl()
        print(f"Metadata for {len(result_list)} acc returned.")

        return result_list.fill_null("NP").write_json(None)  # return metadata results to client
    return render_template('index.html', n_datasets=f"{app.config.metadata['n_datasets']:,}")


@app.route('/advanced', methods=['GET', "POST"])
def advanced():
    if request.method == 'POST':
        # get signatures from fetch/promise API clientside
        form_data = request.get_json()
        # print(f"Form JSON is {sys.getsizeof(form_data)} bytes.")

        # get acc from mastiff (imported from acc.py)
        signatures = form_data['signatures']
        try:
            mastiff_df = getacc(signatures, app.config, http_pool())
        except SearchError as e:
            return e.args

        # get metadata from duckdb
        meta_dic = form_data['metadata']
        meta_list = tuple([
                          key for key, value in meta_dic.items() if value])

        result_list = getduckdb(mastiff_df, meta_list, app.config, duckdb_client(app.config)).pl()
        print(f"Metadata for {len(result_list)} acc returned.")

        return result_list.fill_null("NP").write_json(None)  # return metadata results to client
    return render_template('advanced.html')


@app.route('/about', methods=['GET', "POST"])
def metadata():
    return render_template('about.html', n_datasets=f"{app.config.metadata['n_datasets']:,}")

@app.route('/contact', methods=['GET', "POST"])
def contact():
    return render_template('contact.html')

@app.route('/examples', methods=['GET', "POST"])
def examples():
    # note, fetch call sends to '/' route to return 'simple search' results
    return render_template('examples.html', n_datasets=f"{app.config.metadata['n_datasets']:,}")


# in production this changes:
#
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
