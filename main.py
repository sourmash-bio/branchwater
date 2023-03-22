from flask import Flask, render_template, request

from acc import *
from mongoquery import *
import json


app = Flask(__name__)  # create flask/app instance
app.config['SECRET_KEY'] = 'gibberish'
app.config['UPLOAD_FOLDER'] = 'static/files'


# add ability to access html templates for form with form = +return
# decorator to tell what URL triggers function
@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    if request.method == 'POST':
        form_data = request.get_json()

        # get acc
        signatures = form_data['signatures']
        mastiff_df = getacc(signatures)
        acc_t = tuple(mastiff_df.SRA_accession.tolist())

        # get metadata (needs to be replaced with metadata list from form)
        meta_list = ("acc", "organism", "collection_date_sam",
                     "geo_loc_name_country_calc", "lat_lon_sam")
        meta_json = getmongo(acc_t, meta_list)
        print(f"Metadata for {len(meta_json)} acc returned!")

        # test_json = json.dumps(data_json, indent=4)
        print(meta_json)

        # add containment/merge it in
        # metadata needs nulls to characters before rendering

        return render_template('index.html')
    return render_template('index.html')


@ app.route('/grid', methods=['GET', 'POST'])
def grid():
    return render_template('grid.html')


@ app.route('/api/data')
def data():
    temp_dict = [
        {
            "acc": "ERR3405110",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3404806",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2239124",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR7197562",
            "assay_type": "WGS",
            "organism": "Sus scrofa",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR13502674",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"36.16 N 86.78 W\"]"
        },
        {
            "acc": "SRR13557504",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"36.16 N 86.78 W\"]"
        },
        {
            "acc": "SRR13503148",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"36.16 N 86.78 W\"]"
        },
        {
            "acc": "SRR11276968",
            "assay_type": "WGS",
            "organism": "Ligilactobacillus salivarius",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "ERR3593555",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2367327",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR14000809",
            "assay_type": "WGS",
            "organism": "human metagenome",
            "lat_lon_sam": "[\"55.740813 N 12.544197 E\"]"
        },
        {
            "acc": "SRR11183552",
            "assay_type": "WGS",
            "organism": "pig gut metagenome",
            "lat_lon_sam": "[\"34.1273 S 150.7387 E\"]"
        },
        {
            "acc": "SRR11183817",
            "assay_type": "WGS",
            "organism": "pig gut metagenome",
            "lat_lon_sam": "[\"34.1273 S 150.7387 E\"]"
        },
        {
            "acc": "ERR6196075",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4333869",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR6170279",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR10692830",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"23.33 N 103.36 E\"]"
        },
        {
            "acc": "SRR10680405",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"22.38 N 114.20 E\"]"
        },
        {
            "acc": "SRR13022306",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"40.454 N 79.933 W\"]"
        },
        {
            "acc": "ERR4174824",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR8845349",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"22.27 N 113.46 E\"]"
        },
        {
            "acc": "ERR2855855",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR16681862",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"55.45 N 37.37 E\"]"
        },
        {
            "acc": "ERR7570131",
            "assay_type": "OTHER",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR5194612",
            "assay_type": "WGS",
            "organism": "human nasopharyngeal metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR8452371",
            "assay_type": "WGS",
            "organism": "canine metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "ERR3434419",
            "assay_type": "WGS",
            "organism": "mouse gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR5713948",
            "assay_type": "WGS",
            "organism": "human metagenome",
            "lat_lon_sam": "[\"57.708870 N 11.974560 E\"]"
        },
        {
            "acc": "SRR8634504",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "[\"32.0806 N 34.7898 E\"]"
        },
        {
            "acc": "SRR12823606",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"43.674125 N 72.273013 W\"]"
        },
        {
            "acc": "SRR14251635",
            "assay_type": "WGA",
            "organism": "Escherichia coli",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR15244450",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"46.19 N 9.03 E\"]"
        },
        {
            "acc": "ERR2749996",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2750378",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3335859",
            "assay_type": "OTHER",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR9098019",
            "assay_type": "OTHER",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR15127949",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"43.674125 N 72.273013 W\"]"
        },
        {
            "acc": "ERR3966185",
            "assay_type": "WGS",
            "organism": "viral metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1766292",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR10489616",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"38.91 N 76.96 W\"]"
        },
        {
            "acc": "ERR4623476",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4562308",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2868441",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1539453",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1728167",
            "assay_type": "WGS",
            "organism": "Homo sapiens",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1729223",
            "assay_type": "WGS",
            "organism": "Homo sapiens",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2227642",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR688510",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2017776",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR5651412",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"33.7921 N 84.3214 W\"]"
        },
        {
            "acc": "SRR15237465",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR4423012",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "[\"Not collected\"]"
        },
        {
            "acc": "SRR1162525",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR12934112",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "SRR3131884",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"38.6375 N 90.2651 W\"]"
        },
        {
            "acc": "SRR11553106",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR8993317",
            "assay_type": "OTHER",
            "organism": "synthetic metagenome",
            "lat_lon_sam": "[\"39.1704 N 86.5143 W\"]"
        },
        {
            "acc": "SRR8803184",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "SRR9199315",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"39.57 N 75.11 W\"]"
        },
        {
            "acc": "SRR6262430",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"40.4308 N 79.9598 W\"]"
        },
        {
            "acc": "SRR6837566",
            "assay_type": "WGS",
            "organism": "wastewater metagenome",
            "lat_lon_sam": "[\"1.39 N 103.921 E\"]"
        },
        {
            "acc": "SRR12277007",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"40.49 N 111.41 E\"]"
        },
        {
            "acc": "SRR10212765",
            "assay_type": "WGS",
            "organism": "mouse gut metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "SRR2937624",
            "assay_type": "WGS",
            "organism": "wastewater metagenome",
            "lat_lon_sam": "[\"none\"]"
        },
        {
            "acc": "SRR5056931",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"39.28846263 N 76.62594594 W\"]"
        },
        {
            "acc": "ERR1190713",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "DRR162452",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"34.6850 N 135.1015 E\"]"
        },
        {
            "acc": "ERR3451605",
            "assay_type": "WGS",
            "organism": "human metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR6001921",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR4444792",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"39.28846263 N 76.62594594 W\"]"
        },
        {
            "acc": "ERR4158366",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2597423",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3698124",
            "assay_type": "WGS",
            "organism": "Homo sapiens",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR13061016",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"37.56 N 126.94 E\"]"
        },
        {
            "acc": "SRR8675918",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"29.35 N 106.33 E\"]"
        },
        {
            "acc": "ERR3593781",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3593175",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3593301",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2368252",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR14369187",
            "assay_type": "WGS",
            "organism": "pig gut metagenome",
            "lat_lon_sam": "[\"52.4685 N 113.7307 W\"]"
        },
        {
            "acc": "ERR4678637",
            "assay_type": "WGS",
            "organism": "wastewater metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR17032192",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "SRR10692530",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"25.02 N 102.41 E\"]"
        },
        {
            "acc": "SRR12159253",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"31.23 N 121.47 E\"]"
        },
        {
            "acc": "SRR12159451",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"31.23 N 121.47 E\"]"
        },
        {
            "acc": "SRR10479035",
            "assay_type": "OTHER",
            "organism": "human metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR14882038",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR7124766",
            "assay_type": "WGS",
            "organism": "human metagenome",
            "lat_lon_sam": "[\"39.9 N 116.23 E\"]"
        },
        {
            "acc": "SRR14863641",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "SRR14573982",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"39.54 N 116.28 E\"]"
        },
        {
            "acc": "SRR6323552",
            "assay_type": "WGS",
            "organism": "chicken gut metagenome",
            "lat_lon_sam": "[\"not collected\"]"
        },
        {
            "acc": "SRR17738079",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"38.04 N 84.50 W\"]"
        },
        {
            "acc": "ERR3436437",
            "assay_type": "WGS",
            "organism": "mouse gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR5679013",
            "assay_type": "WGS",
            "organism": "terrestrial metagenome",
            "lat_lon_sam": "[\"40.21 N 104.80 W\"]"
        },
        {
            "acc": "SRR8882787",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"40.2859 N 76.6502 W\"]"
        },
        {
            "acc": "SRR8901672",
            "assay_type": "WGA",
            "organism": "Escherichia coli",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3696566",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2750582",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR13740008",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"41.8786 N 71.3831 W\"]"
        },
        {
            "acc": "SRR13303213",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"not collected\"]"
        },
        {
            "acc": "ERR4570918",
            "assay_type": "WGS",
            "organism": "mouse gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR5169907",
            "assay_type": "OTHER",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR2582246",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "ERR2194114",
            "assay_type": "WGS",
            "organism": "Gallus gallus",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4089517",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4088080",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR17968140",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"45.44 N 126.43 E\"]"
        },
        {
            "acc": "SRR3988583",
            "assay_type": "WGS",
            "organism": "marine metagenome",
            "lat_lon_sam": "[\"48.6000 N 123.5000 W\"]"
        },
        {
            "acc": "SRR5829282",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "[\"39.9 N 116.3 E\"]"
        },
        {
            "acc": "SRR11073050",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"44.016369 N 92.475395 W\"]"
        },
        {
            "acc": "SRR5127603",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"Missing\"]"
        },
        {
            "acc": "SRR6054624",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"Missing\"]"
        },
        {
            "acc": "SRR5950630",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"Missing\"]"
        },
        {
            "acc": "ERR1620324",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1620375",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR652325",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR2191084",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1190586",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR10029215",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR16961786",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"31.27 N 121.45 E\"]"
        },
        {
            "acc": "ERR1398186",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR6002229",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1137048",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR10613533",
            "assay_type": "WGS",
            "organism": "air metagenome",
            "lat_lon_sam": "[\"40.0047 N 116.3261 E\"]"
        },
        {
            "acc": "SRR13836160",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"31 N 121 E\"]"
        },
        {
            "acc": "SRR8891826",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "ERR3404632",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3503314",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR9157888",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"51.8921 N 8.4933 W\"]"
        },
        {
            "acc": "SRR13434593",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"2.9815 S 23.82226 E\"]"
        },
        {
            "acc": "SRR11363006",
            "assay_type": "WGS",
            "organism": "feces metagenome",
            "lat_lon_sam": "[\"32.7157 N 117.1611 W\"]"
        },
        {
            "acc": "ERR3593460",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR14001057",
            "assay_type": "WGS",
            "organism": "human metagenome",
            "lat_lon_sam": "[\"55.740813 N 12.544197 E\"]"
        },
        {
            "acc": "SRR12395644",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"42.98 N 81.24 W\"]"
        },
        {
            "acc": "SRR8960946",
            "assay_type": "WGS",
            "organism": "pig gut metagenome",
            "lat_lon_sam": "[\"34.1273 S 150.7387 E\"]"
        },
        {
            "acc": "SRR11941381",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR11941618",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "ERR4682378",
            "assay_type": "WGS",
            "organism": "wastewater metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR12907781",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"50.886 N 11.62 E\"]"
        },
        {
            "acc": "SRR16646145",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "SRR13318507",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"not collected\"]"
        },
        {
            "acc": "ERR5083956",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR10691960",
            "assay_type": "OTHER",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"25.59 N 99.55 E\"]"
        },
        {
            "acc": "SRR13077673",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"22.38 N 114.2 E\"]"
        },
        {
            "acc": "SRR17643700",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"2.67 N 101.55 E\"]"
        },
        {
            "acc": "SRR17643810",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"5.798 N 100.91 E\"]"
        },
        {
            "acc": "SRR13773631",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"missing\"]"
        },
        {
            "acc": "ERR5004932",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR341665",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR15275213",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"NA\"]"
        },
        {
            "acc": "SRR12159315",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"31.23 N 121.47 E\"]"
        },
        {
            "acc": "SRR5558208",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"41.997742 N 2.820006 E\"]"
        },
        {
            "acc": "SRR15343550",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "[\"not collected\"]"
        },
        {
            "acc": "SRR14251735",
            "assay_type": "WGA",
            "organism": "Escherichia coli",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR5241452",
            "assay_type": "OTHER",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3338964",
            "assay_type": "OTHER",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR5011392",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "[\"44.9739 N 93.2275 W\"]"
        },
        {
            "acc": "SRR6659390",
            "assay_type": "OTHER",
            "organism": "food metagenome",
            "lat_lon_sam": "[\"37.58 N 75.78 W\"]"
        },
        {
            "acc": "ERR2193956",
            "assay_type": "WGS",
            "organism": "Gallus gallus",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR2182419",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4563624",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4561696",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4560949",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR4563027",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "SRR8387646",
            "assay_type": "WGS",
            "organism": "metagenome",
            "lat_lon_sam": "[\"not applicable\"]"
        },
        {
            "acc": "ERR1727920",
            "assay_type": "WGS",
            "organism": "Homo sapiens",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR3160560",
            "assay_type": "WGS",
            "organism": "gut metagenome",
            "lat_lon_sam": "null"
        },
        {
            "acc": "ERR1293634",
            "assay_type": "WGS",
            "organism": "human gut metagenome",
            "lat_lon_sam": "null"
        }
    ]
    return {'data': temp_dict}


if __name__ == '__main__':
    app.run(debug=True)
