from configparser import ConfigParser
import json
import requests
import warnings
from datetime import date, timedelta

config = ConfigParser()
config.read('../config.ini')
api_key = config['meteostat']['key']
default_station_id = config['meteostat']['default_station_id']
use_live_api = bool(config['options']['use_live_api'])
lat = config['options']['lat']
lon = config['options']['lon']
history_range = int(config['options']['history_range'])

# Loads the sample weather-data, used if the api cannot be reached
def get_sample_data():
    with open('../assets/sampleData.json') as json_file:
        return json.load(json_file)

# Tries to query the meteostat api to retrieve the id of the weather-station closest to the provided coordinates
def get_station_id():
    api_url = "https://api.meteostat.net/v1/stations/nearby?lat={}&lon={}&limit=1&key={}".format(
        lat, lon, api_key)
    req = requests.get(api_url)

    if not req.status_code == 200:
        warnings.warn(
            'Unable to reach Meteostat API while trying to retrieve station-id. Using default station-id: ' +
            default_station_id +
            '\nThis can happen when over 200 requests are sent from the same key within 1-hour.',
            Warning,
            stacklevel=2
        )
        return default_station_id

    data = req.json()['data']
    station = data[0]
    id = station['id']
    return id

# Tries to query the meteostat api to retrieve up-to-date weather data
def get_weather_data():
    if not use_live_api:
        warnings.warn('Using sample data. Go to config.ini to turn on live data.', Warning, stacklevel=2)
        return get_sample_data()

    station_id = get_station_id()
    toDate = date.today()
    fromDate = toDate - timedelta(days=history_range)  # 180 Days History
    api_url = "https://api.meteostat.net/v1/history/daily?station={}&start={}&end={}&key={}".format(
        station_id, fromDate, toDate, api_key)
    req = requests.get(api_url)

    if not req.status_code == 200:
        warnings.warn(
            'Unable to reach Meteostat API while trying to retrieve weather data. Using sample-data.\nThis can happen when over 200 requests are sent from the same key within 1-hour.',
            Warning,
            stacklevel=2
        )
        return get_sample_data()

    return req.json()['data']
