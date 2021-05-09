import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd

from api_calls import get_available_crypto_pairs
from config import *
from apps.plotter.dist_plot import total_histogram

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# TODO Change this so that it checks what data is available, rather than just all pairs..

available_pairs = get_available_crypto_pairs(api_key)

relevant_names = available_pairs[['name','symbol']]
relevant_names.rename(columns={'name':'label', 'symbol':'value'}, inplace=True)
dropdown_dict = relevant_names.to_dict('records')

all_dates = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dates_dataframe = pd.DataFrame(all_dates, columns=['label'])
dates_dataframe['value'] = pd.DataFrame(all_dates)
date_dict = dates_dataframe.to_dict('records')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.Graph(id="graph"),
    dcc.Dropdown(
        id='crypto_selector',
        options=dropdown_dict,
        value='BTCUSD'),
    dcc.Dropdown(
        id='date_selector',
        options=date_dict,
        value='All')
])


@app.callback(
    Output("graph", "figure"),
    [Input("crypto_selector", "value"),
     Input("date_selector", "value")])

def display_color(crypto_selector, date_selector):
    data = r"/Users/spencermay/PycharmProjects/crypto_distributions/data/data_store/" + crypto_selector + ".pkl"
    fig = total_histogram(data, date_selector)
    return fig

app.run_server(debug=True)