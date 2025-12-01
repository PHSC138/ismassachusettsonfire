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
# Yes there's a ton of overlap and some overrun into neighboring states, but it's better than not having parts of mass included.
mass = [
    {
        "lat": "42.553249"
        "lng": "-73.118995"
        "rad": "15",
    },
    {
        "lat": "42.530989"
        "lng": "-72.608240"
        "rad": "15",
    },
    {
        "lat": "42.255120"
        "lng": "-71.435701"
        "rad": "16",
    },
    {
        "lat": "41.693766"
        "lng": "-70.389352"
        "rad": "16",
    },
    {
        "lat": "41.393638"
        "lng": "-70.652968"
        "rad": "16",
    },
    {
        "lat": "42.259186"
        "lng": "-73.149123"
        "rad": "17",
    },
    {
        "lat": "42.374947"
        "lng": "-72.069947"
        "rad": "25",
    },
    {
        "lat": "41.975997"
        "lng": "-70.913885"
        "rad": "26",
    },
    {
        "lat": "42.567410"
        "lng": "-70.932948"
        "rad": "22",
    },
    {
        "lat": "42.238855"
        "lng": "-72.726129"
        "rad": "18",
    },
    {
        "lat": "41.978039"
        "lng": "-70.081668"
        "rad": "13",
    },
    {
        "lat": "41.677186"
        "lng": "-69.925147"
        "rad": "11",
    },
    {
        "lat": "41.302743"
        "lng": "-70.139334"
        "rad": "11",
    },
    {
        "lat": "41.592937"
        "lng": "-70.945459"
        "rad": "11",
    },
    {
        "lat": "42.597745"
        "lng": "-71.559080"
        "rad": "10",
    },
    {
        "lat": "42.591595"
        "lng": "-71.357394"
        "rad": "10",
    },
    {
        "lat": "42.602715"
        "lng": "-71.798126"
        "rad": "10",
    },
    {
        "lat": "42.095250"
        "lng": "-71.564839"
        "rad": "10",
    },
    {
        "lat": "42.102065"
        "lng": "-72.358660"
        "rad": "9",
    },
    {
        "lat": "42.137483"
        "lng": "-73.409109"
        "rad": "8",
    },
    {
        "lat": "42.088117"
        "lng": "-71.806486"
        "rad": "8",
    },
    {
        "lat": "42.668384"
        "lng": "-72.368152"
        "rad": "7",
    },
    {
        "lat": "42.675452"
        "lng": "-72.863847"
        "rad": "7",
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


# entry
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
