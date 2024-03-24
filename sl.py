import json
import requests
import datetime


rr_api_key = "9c7f3b82-ddd0-44ff-8ac3-f0a31e730e11"


class stations():

    def __init__(self, update_interval=10):
        self.update_interval = update_interval
        self.stations = [{"name" : "Bredäng",
                          "stop_id": 9289,
                          "rr_stop_id": 740021724,
                          "line": 13,
                          "rr_line": 32,
                          "direction": 1,
                          "rr_direction": 740020757},
                         {"name": "Ålgrytevägen",
                          "stop_id": 1793,
                          "rr_stop_id": 740065618,
                          "line": 163,
                          "rr_line": 128,
                          "direction": 2,
                          "rr_direction": 740000789}]
        self.last_update = datetime.datetime.now()
        self.update()


    def update(self):
        for station in self.stations:
            realtime_departures, json = fetch_departures(station)
            rr_departures, rr_json = fetch_departures_rr(station)


            station['realtime_departures'] = realtime_departures
            station['scheduled_departures'] = rr_departures
            station['json'] = json
            station['rr_json'] = rr_json
        self.last_update = datetime.datetime.now()


    def times_to_next_departures(self):
        """
        This function returns a dictionary. The keys of the dictionary are the
        line numbers of the public transport options tracked by the dashboard.
        The contents of the dictionary items are two lists, the first list
        is of (minutes, seconds) tuples of the time until the next
        departures from the sl API which should give
        realtime transit details.
        The second list is (minutes, seconds) tuples of scheduled departures
        from resrobot.
        """
        if (datetime.datetime.now() - self.last_update).total_seconds() > self.update_interval:
            self.update()

        result = {}
        for station in self.stations:
            this_station = [station['line']]
            realtime_deltas = []
            scheduled_deltas = []
            for departure in station['realtime_departures']:
                delta = departure - datetime.datetime.now()
                realtime_deltas.append(divmod(delta.total_seconds(), 60))
            for departure in station['scheduled_departures']:
                delta = departure - datetime.datetime.now()
                scheduled_deltas.append(divmod(delta.total_seconds(), 60))



            result[station['line']] = [realtime_deltas, scheduled_deltas]
        return result

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

    return estimated_departures, payload

def fetch_departures_rr(station):
    """
    Bredäng = 740021724
    Ålgrytevägen 740065618
    """
    station_id = str(station['rr_stop_id'])
    url = f"https://api.resrobot.se/v2.1/departureBoard"
    params = {'id': station['rr_stop_id'],
              'accessId': rr_api_key,
              'format': 'json',
              'products': station['rr_line'],
              'direction': station['rr_direction'], #code for Ropsten
              'maxJourneys': '5'}

    headers = {'Content-type': 'application/json'}
    r = requests.get(url, params=params, headers=headers, timeout=5)
    payload = r.json()
    scheduled_departures = []
    for departure in payload['Departure']:
        dt = departure['date'] + 'T' + departure['time']
        dep_time =  datetime.datetime.strptime(dt,  '%Y-%m-%dT%H:%M:%S')
        scheduled_departures.append(dep_time)

    return scheduled_departures, payload

def search_station_rr(search_string):
    url = f"https://api.resrobot.se/v2.1/location.name?input={search_string}&format=json&accessId={rr_api_key}"
    params = {'input': search_string,
              'format': "json",
              'accessID': rr_api_key}
    headers = {'Content-type': 'application/json'}
    r = requests.get(url, headers=headers, timeout=5)
    payload = json.loads(r.text)
    return payload
