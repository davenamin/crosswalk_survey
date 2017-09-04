# Daven Amin
# basic Flask Server for leaflet map of Kobo crosswalk survey
# 09/04/2017

import os
import json
import requests
import flask
import memcache

kobo_url = "https://kc.kobotoolbox.org/api/v1/data/"

# important things, passed by environment variable (not secure, sorry!)
kobo_form_id = os.environ['KOBO_FORMID']
user_str = os.environ['KOBO_USER']
pass_str = os.environ['KOBO_PASS']  # ok, i know, i know...

app = flask.Flask(__name__)

# was wishing this could live in just python...
backend = memcache.Client(os.environ['MEMCACHED_URL'])

# let's not hit the kobo API about a billion times, right?
data_stale_timeout = 10  # seconds


# fetch and/or update the latest survey data
def fetch():
    data_cache = backend.get('data')
    if data_cache is None:
        r = requests.get(kobo_url + kobo_form_id, auth=(user_str, pass_str))
        backend.set('data', r.text, time=data_stale_timeout)
        data_cache = backend.get('data')
    return data_cache


# convert a kobo form entry to a geojson feature
def convert_kobo_to_geo(kobo):
    print(kobo.keys())
    return {"type": "Feature",
            "id": kobo['_id'],
            "geometry": {
                "type": "Point",
                "coordinates": [kobo['_geolocation'][1], kobo['_geolocation'][0]]
                },
            "properties": {
                "signal": kobo.get('Is_there_a_pedestrian_crossing_signal', None),
                "marking": kobo.get('How_is_it_marked', None),
                "other": kobo.get('Other_features', None),
                "notes": kobo.get('_notes', None)
                }
            }


# transform data_cache into geojson for leaflet stuff
@app.route("/geojson")
def geojson():
    # check for newer data
    data_cache = json.loads(fetch())
    return json.dumps([convert_kobo_to_geo(k) for k in data_cache])


# render the map!
@app.route("/")
def main():
    return flask.render_template('map.html')


if __name__ == '__main__':
    app.run()
