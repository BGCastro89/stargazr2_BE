import os
import requests
import flask

from datetime import datetime as dt

from helpers import (
    convert_unix_to_YMD,
)


from light_pollution import get_light_pollution
from nearest_csc import get_nearest_csc

VISUAL_CROSSING_API_KEY = os.environ.get('VISUAL_CROSSING_API_KEY', 'XS4YR7QVAR2GL49BHRLLDXHKG')
G_MAPS_API_KEY = os.environ.get('G_MAPS_API_KEY', '')

SUNSET_URL = "https://api.sunrise-sunset.org/json"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
VISUAL_CROSSING_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/%s/%s?key=%s"
GMAPS_ELEV_URL = "https://maps.googleapis.com/maps/api/elevation/json"
GMAPS_DIST_URL = "https://maps.googleapis.com/maps/api/distancematrix/json"


def open_meteo(lat, lng, unix_timestamp):
    """Gets weather at specific lat/lon/time using Open-Meteo API.
    Free for non-commercial use, no API key required (<10,000 calls/day).

    args: lat/lng for location, unix timestamp for desired time
    returns: weather API response in JSON format
    """
    target_hour = dt.utcfromtimestamp(unix_timestamp).strftime("%Y-%m-%dT%H:00")

    params = {
        'latitude': round(lat, 4),
        'longitude': round(lng, 4),
        'hourly': 'precipitation_probability,relative_humidity_2m,cloud_cover,visibility',
        'start_hour': target_hour,
        'end_hour': target_hour,
        'timezone': 'UTC',
    }

    response = requests.get(OPEN_METEO_URL, params=params)
    print(response)
    return response.json()


def gmaps_elevation(lat_selected, lng_selected):
    """Gets the elevation at given coordinates.

    args: lat/lng for stargazing site selcted
    returns: json response with elevation data in meters
    """
    if not G_MAPS_API_KEY:
        raise Exception("Missing API Key for Google Maps")

    elev_params = {
        'locations': str(lat_selected)+","+str(lng_selected),
        'key': G_MAPS_API_KEY
    }

    elev_request = requests.get(GMAPS_ELEV_URL, params=elev_params)
    return elev_request.json()


def gmaps_distance(lat_origin, lng_origin, lat_selected, lng_selected):
    """Gets the distance between two sets of coords

    args: lat/lng for origin and stargazing site selcted
    returns: json response with driving distance (meters) and time (seconds)
    """

    if not G_MAPS_API_KEY:
        raise Exception("Missing API Key for Google Maps")

    dist_params = {
        'origins': str(lat_origin)+","+str(lng_origin),
        'destinations': str(lat_selected)+","+str(lng_selected),
        'key': G_MAPS_API_KEY
    }

    dist_request = requests.get(GMAPS_DIST_URL, params=dist_params)

    return dist_request.json()


def sunrise_sunset_time(lat_selected, lng_selected, time):
    """Gets the times the sun will rise/set, and reach "twilight" conditions sufficent for stargazing

    args: lat/lng for stargazing site selcted
    returns: json response with driving distance (meters) and time (seconds)
    """
    params = {
        'lat': lat_selected,
        'lng': lng_selected,
        'formatted': 0,
        'date': str(convert_unix_to_YMD(time)) if time else "",
    }

    # TODO: Currently only returns darkness times for today, must work for next 48 hours
    # API accepts date paramter but in YYYY-MM-DD format, not unix time
    request = requests.get(SUNSET_URL, params=params)
    return request.json()


def light_pollution(lat_selected, lng_selected):
    """Determines Light Pollution Levels. Internal API.

    args: lat/lng for stargazing site selcted
    returns: json response with light pollution levels (additional brightness ratio)
    """
    return get_light_pollution(float(lat_selected), float(lng_selected))


def nearest_csc(lat_selected, lng_selected):
    """Gets nearest Clear Sky Chart. Internal API.

    args: lat/lng for stargazing site selcted
    returns: json response with the nearest CSC.
    """
    return get_nearest_csc(float(lat_selected), float(lng_selected))
