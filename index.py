#!/usr/bin/env python3

from datetime import datetime
import json
import pathlib
import pytz
import requests
import time

# Boston: 42.3601° N, 71.0589° W
#         42.3601, -71.0589
# Got the most coverage from
#     https://www.freemaptools.com/radius-around-point.htm
mass = [
        {
            "lat": "42.437",
            "lng": "-71.163",
            "rad": "30",
        },
        {
            "lat": "42.400",
            "lng": "-71.669",
            "rad": "25",
        },
        {
            "lat": "42.355",
            "lng": "-72.191",
            "rad": "30",
        },
        {
            "lat": "42.399",
            "lng": "-72.707",
            "rad": "30",
        },
        {
            "lat": "42.391",
            "lng": "-73.240",
            "rad": "30",
        },
        {
            "lat": "41.874",
            "lng": "-70.556",
            "rad": "35",
        }
]


def is_on_fire(coords):
    on_fire = False
    for area in coords:
        r = requests.get(f"https://near-me.airfire.org/near-me/fires?lat={area['lat']}&lng={area['lng']}&maxDistanceMiles={area['rad']}&limit=1")
        try:
            data = r.json()
            if (len(data["fires"]) > 0):
                on_fire= True
                break

        except requests.JSONDecodeError:
            do_error("666")
            exit(1)

    return on_fire


def format_html(on_fire):
    # Le time
    formatted_time = datetime.now(pytz.utc).astimezone(pytz.timezone('America/New_York')).strftime("%a %b %-d %H:%M:%S %Y %Z")

    return f"<html><head><title>Is Massachusetts On Fire?</title></head><body><h1>{'Yes' if on_fire else 'No'}</h1>updated: {formatted_time}</body></html>"


def do_response(html, status_code="200 OK"):
    # Return the custom status
    print(f"Status: {status_code}")
    print("Content-Type: text/html\r\n")
    print(html)
    print("\r\n")

def do_error(code):
    do_response(f"<html><head><title>Is Massachusetts On Fire?</title></head><body><h1>Internal Server Error</h1>Error code: {code}</body></html>", "500 Internal Server Error")


# DO the thingy here
# Get now time in seconds
now = time.time()

# Check for cache file
cache_fname = pathlib.Path("cache.data")
exists = False
mod_time = 0
if (cache_fname.exists()):
    # File exists
    exists = True
    mod_time = cache_fname.stat().st_mtime

# Check if cache exists and was modified less than 5 mins ago
if exists and (now - mod_time < 5 * 60 * 1000):
    # Return cached file
    with open("cache.data", 'r') as fd:
        do_response(fd.read())
else:
    # Create new cached file and return that
    with open("cache.data", 'w+') as fd:
        html = format_html(is_on_fire(mass))
        do_response(html)
        fd.write(html)
