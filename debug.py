"""
Various helper functions for quick and dirty manual testing, debugging, pretty printing, etc

"""

def test_open_meteo_api(weatherdata):
    """DEBUG function for ensuring successful call to Open-Meteo Weather API.

    args: json weatherdata from Open-Meteo API
    returns: None
    """
    print("*********************************")
    if 'error' in weatherdata:
        print("OPEN-METEO API RESPONSE ERROR\n", weatherdata.get('reason', weatherdata['error']))
    elif not weatherdata.get('hourly', {}).get('time'):
        print("OPEN-METEO API RESPONSE ERROR\nNo hourly data returned")
    else:
        print("OPEN-METEO API RESPONSE SUCCESS\n")


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
