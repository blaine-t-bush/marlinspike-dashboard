import json
import requests

def fetch_departures(stop_id=9289):
    """
    9289 = Bredäng station
    1793 = Ålgrytevägen
    """
    url = f"https://transport.integration.sl.se/v1/sites/{stop_id}/departures"
    headers = {'Content-type': 'application/json'}
    params = {'line': "13",
              'direction': "1",
              'forecast': '60'}

    r = requests.get(url, headers=headers, params=params)

    payload = json.loads(r.text)


    return payload


