import requests
import pandas as pd
import os

from config import *
from api_calls import get_daily_prices

# Get all cryptos available on API
response = requests.get(base_url + version + "symbol/available-cryptocurrencies?apikey=" + api_key)
json = response.json()

# Parse response as json and convert to df for readability
available_pairs = pd.DataFrame(json)
print(available_pairs)

failed = 0
count = 0
for crypto_pair in available_pairs['symbol']:
    daily_prices = get_daily_prices(crypto_pair, api_key)
    filename_j = os.path.join(project_root, "data/data_store/" + str(crypto_pair) + ".pkl")
    daily_prices.to_pickle(filename_j)
    count +=1

print(str(count) + " pairs grabbed, " + str(failed) + " pairs failed")