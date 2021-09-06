import requests
import time

curr_time = int(time.time())
SECONDS_IN_DAY = 86400
ENDPOINT_URL = "http://localhost:8085"

def call_endpoint(lat_selected, lng_selected, lat_org=None, lng_org=None, time=None):

    params = {
        'lat_selected': lat_selected,
        'lng_selected': lng_selected,
        'lat_org': lat_org,
        'lng_org': lng_org,
        'time': time,
    }
    request = requests.get(ENDPOINT_URL, params=params)
    print(request)
    return request.json()


def test():
    # Test at Pt Reyes w/o specified user location or time
    print("********** Pt. Reyes TEST w/o time, w/o origin**********")
    result = call_endpoint(38.116947, -122.925357)
    print(result, "\n")

    # # Test at Pt Reyes w/o specified user location, for future time (No driving or CSC returned)
    print("********** Pt. Reyes TEST w/o origin, in 2 days**********")
    result = call_endpoint(38.116947, -122.925357, None, None, time + SECONDS_IN_DAY*2)
    print(result, "\n")

    # # Test San Francisco as user location, Stony Gorge at stargazing site, no time specified (now)
    print("********** SF to Pt. Reyes TEST w/o time (now) **********")
    result = call_endpoint(37.7360512, -122.4997348, 38.116947, -122.925357)
    print(result, "\n")

    # Test San Francisco as user location, Stony Gorge at stargazing site, time is in 12 hr
    print("********** SF-Stony Gorge w/ time **********")
    result = call_endpoint(37.7360512, -122.4997348, 39.580110, -122.524105, curr_time + SECONDS_IN_DAY/2)
    print(result, "\n")

    # # Test San Francisco as user location, Pt Reyes at stargazing site, time is in 24 hr
    print("********** SF-Pt. Reyes w/ time **********")
    result = call_endpoint(37.7360512, -122.4997348, 38.116947, -122.925357, time + SECONDS_IN_DAY)
    print(result, "\n")

    # # Test San Francisco as user location, Stony Gorge at stargazing site, time is in 36 hr
    print("********** SF-Stony Gorge w/ time **********")
    result = call_endpoint(37.7360512, -122.4997348, 39.580110, -122.524105, time + SECONDS_IN_DAY*1.5)
    print(result, "\n")

if __name__ == "__main__":
    test()