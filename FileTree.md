**app** – files to run flask app; flask backend, frontend is
html/vanilla javascript, including plotly.js, tabulator.js, bootswatch.js

 ├── Dockerfile – docker build for app

 ├── config.yml – app config

 ├── functions.py – functions used in flask/backend

 ├── main.py – flask instance definition

─ **static**

 ├── dashboard.js – js function to build interactive table, histograms, and maps

 ├── ex_sig.js – preprocessed signatures for example page

 ~~├~~~~── fetchandplot.js~~

 ├── formdata.js – generated from metadata_prep/createform.py for use on Advanced webpage

 ~~├~~~~── forms.js~~

 ~~├~~~~── metadata_table.js~~

 ├── mgnify-component – contains necessary files for EBI component

 ~~└── testdash.js~~

─ **templates** – contains all html templates for page

 ├── about.html

 ├── advanced.html – relies on: fetchandplot.js (formdata.js), dashboard.js

 ├── examples.html – relies on: ex_sig.js, fetchandplot.js (formdata.js), dashboard.js

 ├── footer.html

 ├── header.html

 ├── index.html – relies on: fetchandplot.js (formdata.js), dashboard.js


**buildmongo** – creates read-only mongob metadata of
accession metadata from big query

 ├── Dockerfile

 ├── README.md

 ├── attrcounts_4.5percent.csv – built with metadata_prep/count_attr.py

 ├── bqKey.json – Big Query key for account

 ├── bqtomongo.py – builds mongo-DB; Relies on bqKey.json and attrcounts_4.5percent.csv

 ├── config.yml

 ~~├~~~~── keypath.py~~

├── sra.runinfo.csv

├── docker-compose.debug.yml

├── docker-compose.yml


**metadata_prep** – preps metadata for buildmongo and html forms,
see readme for description

 ├── attrcounts.csv

 ├── attrcounts_4.5percent.csv

 ├── attrcounts_4.5percent_manualcategories.csv

 ├── attributeList.csv

 ├── count_attr.py

 ├── createform.py

 └── sra.runinfo.csv
