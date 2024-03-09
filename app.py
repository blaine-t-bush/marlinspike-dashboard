import os
import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from flask import Flask, render_template


app = Flask(__name__)

@dataclass
class Weather:
  air_temperature: float
  precipitation_rate: float
  wind_speed: float
  wind_speed_of_gust: float
  wind_from_direction: float

load_dotenv()
LOC_LAT = os.getenv('LOC_LAT', None)
LOC_LON = os.getenv('LOC_LON', None)
if LOC_LAT is None:
  raise EnvironmentError('Could not parse latitude from environment variables. Make sure the LOC_LAT environment variable is set.')
if LOC_LON is None:
  raise EnvironmentError('Could not parse latitude from environment variables. Make sure the LOC_LON environment variable is set.')

def get_weather() -> Weather:
  response = requests.get(f'https://api.met.no/weatherapi/nowcast/2.0/complete?lat={LOC_LAT}&lon={LOC_LON}', headers={
    'User-Agent': 'https://github.com/blaine-t-bush/marlinspike-dashboard'
  })
  if response.status_code == 200:
    data_now = response.json()["properties"]["timeseries"][0]["data"]["instant"]["details"]
    return Weather(data_now["air_temperature"],
                      data_now["precipitation_rate"],
                      data_now["wind_speed"],
                      data_now["wind_speed_of_gust"],
                      data_now["wind_from_direction"])
  return Weather()


@app.route('/')
def index():
  weather_data = get_weather()
  return render_template('index.html', data=weather_data)


if __name__ == '__main__':
  app.run(debug=True)
