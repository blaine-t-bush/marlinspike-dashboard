import os
import weather
from dotenv import load_dotenv
from flask import Flask, render_template


app = Flask(__name__)

load_dotenv()
LOC_LAT = os.getenv('LOC_LAT', None)
LOC_LON = os.getenv('LOC_LON', None)
if LOC_LAT is None:
  raise EnvironmentError('Could not parse latitude from environment variables. Make sure the LOC_LAT environment variable is set.')
if LOC_LON is None:
  raise EnvironmentError('Could not parse latitude from environment variables. Make sure the LOC_LON environment variable is set.')


@app.route('/')
def index():
  return render_template('index.html', weather_data=weather.get_weather(lat=LOC_LAT, lon=LOC_LON))


if __name__ == '__main__':
  app.run(debug=True)
