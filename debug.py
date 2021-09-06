"""
Various helper functions for quick and dirty manual testing, debugging, pretty printing, etc

"""


def test_DS_api(weatherdata):
    """DEBUG function for ensuring sucessful call to DarkSky Weather API.

    args: json weatherdata from DarkSky API
    returns: None
    """
    print("*********************************")
    if 'error' in weatherdata.keys():
        print("DARKSKY API RESPONSE ERROR\nHTTP", weatherdata['code'], "-", weatherdata['error'])
    else:
        print("DARKSKY API RESPONSE SUCESS\n")


def pp_when_in_day_night_cycle(darkness_times, curr_time_unix):
    """Pretty prints current time in relation to darkness start/stop times

    args: unix timestamp for current time, morning darkness ends, night darkness begins
    returns: None
    """
    times = {
        'prev stargaze_start': int(darkness_times['prev_day_dusk']),
        'stargaze_end       ': int(darkness_times['curr_day_dawn']),
        '***curr_time***    ': int(curr_time_unix),
        'stargaze_start     ': int(darkness_times['curr_day_dusk']),
        'next stargaze_end  ': int(darkness_times['next_day_dawn']),
        'next stargaze_start': int(darkness_times['next_day_dusk']),
    }
    print("********* When Current time is in Day/Night Cycle? *********")
    for key, value in sorted(list(times.items()), key=lambda x: x[1]):
        print("%s: %s" % (key, value))


def pp_site_rating_breakdown(precipProbability, humidity, cloudCover, lightPol, precip_quality, humid_quality, cloud_quality, lightpol_quality, site_quality_rating):
    print("********* Site Rating Breakdown *********")
    print("precipProbability:", precipProbability, ">", str(round(precip_quality*100, 1))+"%")
    print("humidity:", humidity, ">", str(round(humid_quality*100, 1))+"%")
    print("cloudCover:", cloudCover, ">", str(round(cloud_quality*100, 1))+"%")
    print("lightPol:", lightPol, ">", str(round(lightpol_quality*100, 1))+"%")
    print("site_quality_rating:", str(round(site_quality_rating, 1))+"%\n")

# TODO: Move to/create dedicated tests
# def smoke_test():
#     time = get_current_unix_time()

#     # Test at Pt Reyes w/o specified user location or time
#     result = get_stargaze_report(None)
#     print("********** Pt. Reyes TEST w/o time, w/o origin**********")
#     print(result, "\n")

#     # Test at Pt Reyes w/o specified user location, for future time (No driving or CSC returned)
#     result = get_stargaze_report(38.116947, -122.925357, None, None, time + SECONDS_IN_DAY*2)
#     print("********** Pt. Reyes TEST w/o origin, in 2 days**********")
#     print(result, "\n")

#     # Test San Francisco as user location, Stony Gorge at stargazing site, no time specified (now)
#     result = get_stargaze_report(37.7360512, -122.4997348, 38.116947, -122.925357)
#     print("********** SF to Pt. Reyes TEST w/o time (now) **********")
#     print(result, "\n")

#     # Test San Francisco as user location, Stony Gorge at stargazing site, time is in 12 hr
#     result = get_stargaze_report(37.7360512, -122.4997348, 39.580110, -122.524105, time + SECONDS_IN_DAY/2)
#     print("********** SF-Stony Gorge w/ time **********")
#     print(result, "\n")

#     # Test San Francisco as user location, Pt Reyes at stargazing site, time is in 24 hr
#     result = get_stargaze_report(37.7360512, -122.4997348, 38.116947, -122.925357, time + SECONDS_IN_DAY)
#     print("********** SF-Pt. Reyes w/ time **********")
#     print(result, "\n")

#     # Test San Francisco as user location, Stony Gorge at stargazing site, time is in 36 hr
#     result = get_stargaze_report(37.7360512, -122.4997348, 39.580110, -122.524105, time + SECONDS_IN_DAY*1.5)
#     print("********** SF-Stony Gorge w/ time **********")
#     print(result, "\n")
