import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

prices_file = r"C:\Users\spenc\PycharmProjects\BTC_Seasonality\BTC_USD_2013-10-01_2021-03-26-CoinDesk.csv"

# Import daily BTC price
btc_prices = pd.read_csv(prices_file, index_col=1)

# Simplify just to close price for this purpose
btc_close = btc_prices['Closing Price (USD)']

# Drop index to use for function
btc_close_noidx = btc_close.reset_index()

# Change to datetime for .dt
btc_close_noidx['Date'] = pd.to_datetime(btc_close_noidx['Date'])

# Add day names
btc_close_noidx['day_of_week'] = btc_close_noidx['Date'].dt.day_name()

# Add returns column
btc_close_noidx['daily_returns'] = btc_close_noidx['Closing Price (USD)'].pct_change()

daysofweek = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Set up plotly dashboard page (Aggregated, then days of week)
fig = make_subplots(rows=2, cols=4,
                    subplot_titles=('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))

# Make list of values for table
mean=[]
std=[]
skew=[]
kurt=[]

# Get returns distribution for each day of week. Rename columns for later purposes

i=0
for dow in daysofweek:
    # Get position of subplot
    i += 1
    print(i)
    if i<5:
        row=1
        col=i
    else:
        row = 2
        col = i-4

    if dow == 'All':
        btc_close_noidx_plot = btc_close_noidx[['Date', 'daily_returns']]
        btc_close_noidx_plot = btc_close_noidx_plot.rename({'daily_returns': 'All'}, axis=1)
        fig.append_trace(go.Histogram(x=btc_close_noidx_plot['All']), row=row, col=col)

    # Filter df by day of week
    filtered_btc = btc_close_noidx.loc[btc_close_noidx['day_of_week'] == dow]

    # Reduce to what we need
    filtered_btc_clean = filtered_btc[['Date', 'daily_returns']]
    filtered_btc_clean.columns.name = dow
    filtered_btc_clean_plot = filtered_btc_clean.rename({'daily_returns': dow}, axis=1)


    # Get sample stats for each df
    if i ==1:
        day_mean = btc_close_noidx_plot.mean(numeric_only=True)
        day_std = btc_close_noidx_plot.std(numeric_only=True)
        day_skew = btc_close_noidx_plot.skew(numeric_only=True)
        day_kurt = btc_close_noidx_plot.kurtosis(numeric_only=True)

    else:
        day_mean = filtered_btc_clean_plot.mean(numeric_only=True)
        day_std = filtered_btc_clean_plot.std(numeric_only=True)
        day_skew = filtered_btc_clean_plot.skew(numeric_only=True)
        day_kurt= filtered_btc_clean_plot.kurtosis(numeric_only=True)

    # Histogram each dist on one page

    fig.append_trace(go.Histogram(x=filtered_btc_clean_plot[dow]), row=row, col=col)

    # Add to lists for table
    mean.append(day_mean[0])
    std.append(day_std[0])
    skew.append(day_skew[0])
    kurt.append(day_kurt[0])

# Create table to add at bottom from df

sample_stats = pd.DataFrame(
    {'mean': mean,
     'std': std,
     'skew': skew,
     'kurt' : kurt
    }, index=daysofweek)



fig.update_layout(title_text="BTC Price Returns (USD) by Day of Week", showlegend=False)
fig.show()






