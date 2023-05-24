import pandas as pd
import html
import csv
import json


def generate_form_html(csv_file_path, js_file_path):
    df = pd.read_csv(csv_file_path)

    # Sort by 'HarmonizedName'
    # later sort by 'metadata_category' column
    df = df.sort_values(
        by=['metadata_category', 'HarmonizedName'], ascending=[False, True])
    form = ""
    checked_str = ""
    current_category = None

    for _, d in df.iterrows():
        # checked_str += f"{d['HarmonizedName']}: form.elements.{d['HarmonizedName']}.checked,\n"
        # html += f"<div style='display:inline-block; width:25%;'><label><input type='checkbox' name='{d['HarmonizedName']}' id='{d['HarmonizedName']}'><strong>{d['HarmonizedName']}</strong> - ({round(d['percentage'])}%) </label><br></div>"
        if d['metadata_category'] != current_category:
            current_category = d['metadata_category']

            # Add a heading for the category
            form += f"<br/><br/><h5 class='text-success'>{current_category}</h5>"

        # Escape special characters in NCBI_provided_description
        ncbi_description = html.escape(d['NCBI_provided_description'])

        form += f"<div style='display:inline-block; width:25%;'><label data-bs-toggle='tooltip' data-bs-placement='bottom' title='{ncbi_description}'><input type='checkbox' name='{d['HarmonizedName']}' id='{d['HarmonizedName']}'><strong>{d['HarmonizedName']}</strong> - ({round(d['percentage'])}%) </label><br></div>"
        checked_str += f"{d['HarmonizedName']}: form.elements.{d['HarmonizedName']}.checked,\n"

    # remove the first two breaks from the form
    form = form.replace("<br/>", "", 2)

    js_code = f"let html = \"{form}\";\n\nlet checked_str = {{{checked_str}}};"

    with open(js_file_path, 'w') as js_file:
        js_file.write(js_code)


generate_form_html("metadata_prep/attrcounts_4.5percent_manualcategories.csv",
                   "app/static/formdata.js")


def generate_table_js(csv_file_path):
    selected_columns = ['HarmonizedName',
                        'NCBI_provided_description', 'percentage']

    # Read the CSV file and create the metadata table
    metadata_table = []
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create a dictionary with only the selected columns
            selected_data = {column: row[column]
                             for column in selected_columns}
            metadata_table.append(selected_data)

        # Convert metadata table to a JSON string
    json_string = json.dumps(metadata_table, indent=2)

    # Write the JSON string to a JavaScript file
    js_file = 'app/static/metadata_table.js'
    with open(js_file, 'w') as file:
        file.write('const metadata_table = ')
        file.write(json_string)

    print(f'Successfully created {js_file} with the metadata.')


generate_table_js("metadata_prep/attrcounts_4.5percent_manualcategories.csv")
