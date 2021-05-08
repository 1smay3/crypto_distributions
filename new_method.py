import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

prices_file = r"C:\Users\spenc\PycharmProjects\BTC_Seasonality\BTC_USD_2013-10-01_2021-05-03-CoinDesk.csv"

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



fig = make_subplots(
    rows=3, cols=4,
    horizontal_spacing=0.03,
    vertical_spacing=0.05,
    specs=[[{}, {}, {}, {}],
           [{}, {}, {}, {}],
           [{"rowspan" :1, "colspan": 4, "type": "table"}, None, None, None]],print_grid=True,
                subplot_titles=('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))

# Make list of values for table
mean=[]
median=[]
std=[]
skew=[]
kurt=[]
sample_size_list=[]
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
        fig.append_trace(go.Histogram(x=btc_close_noidx_plot['All'], histnorm='probability'), row=row, col=col)

    # Filter df by day of week
    filtered_btc = btc_close_noidx.loc[btc_close_noidx['day_of_week'] == dow]

    # Reduce to what we need
    filtered_btc_clean = filtered_btc[['Date', 'daily_returns']]
    filtered_btc_clean.columns.name = dow
    filtered_btc_clean_plot = filtered_btc_clean.rename({'daily_returns': dow}, axis=1)


    # Get sample stats for each df
    if i ==1:
        day_mean = btc_close_noidx_plot.mean(numeric_only=True)
        day_median = btc_close_noidx_plot.median(numeric_only=True)
        day_std = btc_close_noidx_plot.std(numeric_only=True)
        day_skew = btc_close_noidx_plot.skew(numeric_only=True)
        day_kurt = btc_close_noidx_plot.kurtosis(numeric_only=True)
        sample_size = len(btc_close_noidx_plot)

    else:
        day_mean = filtered_btc_clean_plot.mean(numeric_only=True)
        day_median = filtered_btc_clean_plot.median(numeric_only=True)
        day_std = filtered_btc_clean_plot.std(numeric_only=True)
        day_skew = filtered_btc_clean_plot.skew(numeric_only=True)
        day_kurt= filtered_btc_clean_plot.kurtosis(numeric_only=True)
        sample_size = len(filtered_btc_clean_plot)
    # Histogram each dist on one page

    fig.append_trace(go.Histogram(x=filtered_btc_clean_plot[dow], histnorm='probability'), row=row, col=col)

    # Add to lists for table
    mean.append('{:.2%}'.format(day_mean[0]))
    median.append('{:.2%}'.format(day_median[0]))
    std.append('{:.2%}'.format(day_std[0]))
    skew.append('{:.3}'.format(day_skew[0]))
    kurt.append('{:.3}'.format(day_kurt[0]))
    sample_size_list.append('{:1}'.format(sample_size))

# Create table to add at bottom from df

sample_stats = pd.DataFrame(
    {'Mean': mean,
     'Median': median,
     'Standard Deviation': std,
     'Skew': skew,
     'Kurtosis' : kurt,
     'Sample Size': sample_size_list
    }, index=daysofweek)

sample_stats_labeled = sample_stats.reset_index()
sample_stats_labeled = sample_stats_labeled.rename({'index': "Day of Week"}, axis=1)


fig.add_trace(go.Table(
    header=dict(values=list(sample_stats_labeled.columns),

                align='center'),
    cells=dict(values=[sample_stats_labeled['Day of Week'], sample_stats_labeled['Mean'], sample_stats_labeled['Median'],
                       sample_stats_labeled['Standard Deviation'], sample_stats_labeled['Skew'], sample_stats_labeled['Kurtosis'],
                       sample_stats_labeled['Sample Size']],

               align='center'))
, row=3, col=1)

fig.update_layout(title_text="BTC Price Returns (USD) by Day of Week", showlegend=False)
fig.show()


# TODO make x and y axis percentage
# TODO add button to change between PDF and CDF: https://plotly.com/python/custom-buttons/#update-button




