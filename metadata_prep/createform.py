import pandas as pd


def generate_form_html(csv_file_path):
    df = pd.read_csv(csv_file_path)

    # Sort by 'HarmonizedName'
    # later sort by 'metadata_category' column
    df = df.sort_values(by='HarmonizedName')
    html = ""
    checked_str = ""

    for _, d in df.iterrows():
        checked_str += f"{d['HarmonizedName']}: form.elements.{d['HarmonizedName']}.checked, "
        html += f"<div style='display:inline-block; width:25%;'><label><input type='checkbox' name='{d['HarmonizedName']}' id='{d['HarmonizedName']}'><strong>{d['HarmonizedName']}</strong> - ({round(d['percentage'])}%) </label><br></div>"

    return html, checked_str


html, checked_str = generate_form_html("static/attrcounts_4.5percent.csv")
print(html)
print(checked_str)
