from pathlib import Path
import pandas as pd
import json
import os
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__)
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_folder = 'static'
app.config['DEBUG']=False

@app.route('/')
def main_page():

    pd.set_option('precision', 2)

    rolling_avg_data = read_rolling_avg()

    xg_data = rolling_avg_data.pivot('team', 'month', 'npxG_roll_adj')
    col1 = xg_data.columns.to_list()[-1]
    xg_data.sort_values(col1, ascending=False, inplace=True)
    # xg_data.reset_index(inplace=True) --> xg_data.to_json(orient='records')
    npxG_roll = xg_data.style\
        .background_gradient(cmap='YlGn')\
        .set_table_attributes("style='width:100%'")\
        .set_caption('npxG (rolling 12 games avg*) in EPL over the last calendar year')\
        .render()

    xgc_data = rolling_avg_data.pivot('team', 'month', 'npxGC_roll_adj')
    col1 = xgc_data.columns.to_list()[-1]
    xgc_data.sort_values(col1, ascending=True, inplace=True)
    # xg_data.reset_index(inplace=True) --> xg_data.to_json(orient='records')
    npxGC_roll = xgc_data.style\
        .background_gradient(cmap='OrRd')\
        .set_table_attributes("style='width:100%'")\
        .set_caption('npxG conceded (rolling 12 games avg*) in EPL over the last calendar year')\
        .render()

    xgd_data = rolling_avg_data.pivot('team', 'month', 'npxGD_roll_adj')
    col1 = xgd_data.columns.to_list()[-1]
    xgd_data.sort_values(col1, ascending=False, inplace=True)
    # xg_data.reset_index(inplace=True) --> xg_data.to_json(orient='records')
    npxGD_roll = xgd_data.style\
        .background_gradient(cmap='RdBu')\
        .set_table_attributes("style='width:100%'")\
        .set_caption('npxG conceded (rolling 12 games avg*) in EPL over the last calendar year')\
        .render()

    content = {
        'viz1': {
            'npxG_roll': npxG_roll,
            'npxGC_roll': npxGC_roll,
            'npxGD_roll': npxGD_roll
        }
    }
    return render_template('index.html', **content)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


def read_rolling_avg():
    base = Path()
    df = pd.read_csv(base / "data/roll_avg.csv", index_col=0)
    return df

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 9001))
    debug = os.environ.get("DEBUG", True)
    print(f"Starting app at port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
