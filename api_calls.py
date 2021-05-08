import requests
import pandas as pd

from config import *



def get_daily_prices(curreny_pair,api_key):
    response = requests.get(base_url + version + "historical-price-full/" + curreny_pair + "?apikey=" + api_key)
    json = response.json()
    # Take the first index as data comes down with symbol at top
    # Parse response as json and convert to df for readability
    filtered_json = json['historical']
    daily_data = pd.DataFrame(filtered_json)
    print(str(curreny_pair) + ": complete!")
    return daily_data