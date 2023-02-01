from flask import Flask, render_template, make_response
from flask_wtf import FlaskForm


from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename  # installed with flasks

from forms import *
# from routes import *

import os
from acc import *
from bigquery import *


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
    form = UploadFileForm()  # this uploads the file after the post request from index.html
# following is the code to actually upload the file
    if form.validate_on_submit():
        file = form.file.data  # first grab the file and make it equal to file varible
        # then save the file
        # os language is getting the route to the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], secure_filename(file.filename))

        acc_t = getacc(filepath)
        meta_list = f"acc, assay_type, organism"

        meta_df = getmeta(acc_t, meta_list)

        # the following may return a CSV; add commented out lines to make it export the csv
        resp = make_response(meta_df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
        # return render_template('index2.html')
        # return f'Uploaded:{file.filename}'

    # returns index.html when home is visited
    return render_template('index.html', form=form)


# a way to run our app, need debug=True because in development mode
if __name__ == '__main__':
    app.run(debug=True)
