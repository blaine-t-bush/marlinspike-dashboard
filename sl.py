import json
import requests
import datetime


rr_api_key = "9c7f3b82-ddd0-44ff-8ac3-f0a31e730e11"


class stations():

    def __init__(self, update_interval=10):
        self.update_interval = update_interval
        self.stations = [{"name" : "Bredäng",
                          "stop_id": 9289,
                          "line": 13,
                          "direction": 1},
                         {"name": "Ålgrytevägen",
                          "stop_id": 1793,
                          "line": 163,
                          "direction": 2}]
        self.last_update = datetime.datetime.now()
        self.update()


    def update(self):
        for station in self.stations:
            next_departures = fetch_departures(station)
            station['departures'] = next_departures

        self.last_update = datetime.datetime.now()

    def times_to_next_departures(self):
        if (datetime.datetime.now() - self.last_update).total_seconds > self.update_interval:
            self.update()

        result = []
        for station in self.stations:
            this_station = [station['line']]
            for departure in station['departures']:
                pass

            result.append([station['line'], station['departures']])


def fetch_departures(station):
    """
    9289 = Bredäng station
    1793 = Ålgrytevägen
    """
    stop_id = station['stop_id']
    url = f"https://transport.integration.sl.se/v1/sites/{stop_id}/departures"
    headers = {'Content-type': 'application/json'}
    params = {'line': str(station['line']),
              'direction': str(station['direction']),
              'forecast': '120'}

    r = requests.get(url, headers=headers, params=params, timeout=5)

    payload = json.loads(r.text)

    estimated_departures = []
    for i in payload['departures']:
        estimated_departures.append(
            datetime.datetime.strptime(i['expected'], '%Y-%m-%dT%H:%M:%S'))

    return estimated_departures

def fetch_departures_rr(station):
    """
    Bredäng = 740021724
    Ålgrytevägen 740065618
    """
    station_id = 740021724
    url = f"https://api.resrobot.se/v2.1/departureBoard?id={station_id}&format=json&accessId={rr_api_key}"
    params = {'products': str(32),
              'direction': "740020757", #code for Ropsten
              'maxJourneys': '3'}

    headers = {'Content-type': 'application/json'}
    r = requests.get(url, params=params, headers=headers, timeout=5)
    payload = json.loads(r.text)
    return payload

def search_station_rr(search_string):
    url = f"https://api.resrobot.se/v2.1/location.name?input={search_string}&format=json&accessId={rr_api_key}"
    params = {'input': search_string,
              'format': "json",
              'accessID': rr_api_key}
    headers = {'Content-type': 'application/json'}
    r = requests.get(url, headers=headers, timeout=5)
    payload = json.loads(r.text)
    return payload
