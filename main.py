from flask import Flask, render_template, make_response, request
from flask_wtf import FlaskForm


from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename

from forms import *

import os
from acc import *
from bigquery import *
import json


app = Flask(__name__)  # create flask/app instance
# db = SQLAlchemy(app)
# secret key to use CSRF token with upload form
app.config['SECRET_KEY'] = 'gibberish'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # max 16mb


# add ability to access html templates for form with form = +return
# decorator to tell what URL triggers function
@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
  # Request.get_json loads a string. json.loads converts it to a list, but all of the data is in spot 0
    if request.method == 'POST':
        siglist = request.get_json()

        acc_t = getacc(siglist)

        meta_list = f"acc, assay_type, organism"
        meta_df = getmeta3(acc_t, meta_list)

        print(
            f"Metadata for {len(meta_df)} acc returned!")
        meta_df.to_csv('bigq.csv')
        resp = make_response(meta_df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return render_template('index.html')


@app.route('/signature', methods=['GET', "POST"])
def signature():
    if request.method == 'POST':
        signatures = request.get_json()
        print(f'AJAX call worked')
        print(signatures)
        print(type(signatures))
       # acc_t = getacc(signatures)
        return {
            'response': 'I am the response'
        }
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
