import pandas as pd
import plotly.graph_objects as go

def total_histogram(pickle_data, dow):
    # Import daily BTC price
    btc_prices = pd.read_pickle(pickle_data)
    btc_prices.set_index("date", inplace=True)
    btc_prices.sort_index(ascending=True, inplace=True)

    # Simplify just to close price for this purpose=
    btc_close = btc_prices['adjClose']

    # Drop index to use for function
    btc_close_noidx = btc_close.reset_index()

    # Change to datetime for .dt
    btc_close_noidx['date'] = pd.to_datetime(btc_close_noidx['date'])

    # Add day names
    btc_close_noidx['day_of_week'] = btc_close_noidx['date'].dt.day_name()

    # Add returns column
    btc_close_noidx['daily_returns'] = btc_close_noidx['adjClose'].pct_change()

    # Plot Histogram of returns depending on day of week
    if dow == 'All':
        rel_hist = go.Figure(data=[go.Histogram(x=btc_close_noidx['daily_returns'])])
    else:
    # Filter dataframe just to day of week
        partial_data = btc_close_noidx.loc[btc_close_noidx['day_of_week'] == dow]
        rel_hist = go.Figure(data=[go.Histogram(x=partial_data['daily_returns'])])
    return rel_hist


