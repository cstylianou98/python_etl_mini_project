import openmeteo_requests

import requests_cache
import pandas as pd
import os
import matplotlib.pyplot as plt
import sqlite3

from retry_requests import retry
from functions import *

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
	"latitude": 35.1753,
	"longitude": 33.3642,
	"start_date": "1998-09-11",
	"end_date": "1999-09-11",
	"hourly": ["temperature_2m", "relative_humidity_2m"],
	"daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"],
	"timezone": "auto"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location.
response = responses[0]

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

hourly_dataframe = pd.DataFrame(data = hourly_data)


# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_mean = daily.Variables(2).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["temperature_2m_mean"] = daily_temperature_2m_mean

daily_dataframe = pd.DataFrame(data = daily_data)


# tuple storing max, min and mean temperatures from 11/09/1998 - 11/09/1999
daily_date = daily_data['date'] 
daily_temperature_tuple = (daily_temperature_2m_max, daily_temperature_2m_min, daily_temperature_2m_mean)


# saving fig, creating folder if it doesn't exist
folder_path = './plots'
file_names = ['max_temp_vs_time', 'min_temp_vs_time', 'mean_temp_vs_time']
legend_names = ['Max', 'Min', 'Mean']

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

plot_temp_graphs(daily_date , daily_temperature_tuple, folder_path, file_names, legend_names)

# Connect to SQLite database (it creates one if it doesn't exist)
connection_db = sqlite3.connect('weather_data.db')
c = connection_db.cursor()

# Create tables if they don't already exist
c.execute('''
    CREATE TABLE IF NOT EXISTS hourly_data (
        date TEXT PRIMARY KEY,
        temperature REAL,
        humidity REAL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS daily_data (
        date TEXT PRIMARY KEY,
        temperature_max REAL,
        temperature_min REAL,
        temperature_mean REAL
    )
''')

# Insert processed data
hourly_dataframe.to_sql('hourly_data', connection_db, if_exists='replace', index=False)
daily_dataframe.to_sql('daily_data', connection_db, if_exists='replace', index=False)

# Commit and close the connection
connection_db.commit()
connection_db.close()

print('The columns titles found in the daily relational database are:') 
print('-----------------------------------------------------------------')
print(daily_dataframe.columns)
print('-----------------------------------------------------------------\n')

## example query
connection_db = sqlite3.connect('weather_data.db')
query = '''
    SELECT date, temperature_2m_mean FROM daily_data
    WHERE date BETWEEN '1999-01-01' AND '1999-12-31'
'''
result = pd.read_sql_query(query, connection_db)
connection_db.close()

print('Example query result is:') 
print('-----------------------------------------------------------------')
print(result)
print('-----------------------------------------------------------------')
