import requests
from dataclasses import dataclass

@dataclass
class Weather:
  air_temperature: float
  precipitation_rate: float
  wind_speed: float
  wind_speed_of_gust: float
  wind_from_direction: float

def get_weather(lat: float = 59.0, lon: float = 18.0) -> Weather:
  response = requests.get(f'https://api.met.no/weatherapi/nowcast/2.0/complete?lat={lat}&lon={lon}', headers={
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