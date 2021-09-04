import requests
import os
import math

from PIL import Image

"""
Light Pollution Coloring Key
Bortle  Color       RGB                LPX              Description
1       Black       (0,0,0)            0.00 - 0.01      Theoretically darkest sky limited by airglow and starlight
2       Dk Gray     (26,26,26)         0.01 - 0.06      Gegenschein visible. Zodiacal light annoyingly bright. Rising milkyway confuses some into thinking it's dawn. Limiting magnitude 7.6 to 8.0 for people with exceptional vision. Users of large dobsonian telescopes are very happy. [-ad]
2       Lt Gray     (54,54,54)         0.06 - 0.11      Faint shadows cast by milkyway visible on white objects. Clouds are black holes in the sky. No light domes. The milky way has faint extentions making it 50 degrees thick. Limiting magntiude 7.1 to 7.5. [-ad]
3       Dk Blue     (0,20,132)         0.11 - 0.19
3       Lt Blue     (0,38,249)         0.19 - 0.33      The sky is crowded with stars, extending to the horizon in all directions. In the absence of haze the M.W. can be seen to the horizon. Clouds appear as black silhouettes against the sky. Stars look large and close. [-Richard Berry] Low light domes (10 to 15 degrees) on horizon. M33 easy with averted vision. M15 is naked eye. Milky way shows bulge into Ophiuchus. Limiting magnitude 6.6 to 7.0. [-ad]
4       Dk Green    (57,129,20)        0.33 - 0.58      a glow in the direction of one or more cities is seen on the horizon. Clouds are bright near the city glow. [-Richard Berry]
4       Md Green    (108,244,38)       0.58 - 1.00      Zodiacal light seen on best nights. Milkyway shows much dark lane structure with beginnings of faint bulge into Ophiuchus. M33 difficult even when above 50 degrees. Limiting magnitude about 6.2 to 6.5. [-ad]
4.5     Green       (179,174,30)       1.00 - 1.73      The M.W. is brilliant overhead but cannot be seen near the horizon. Clouds have a greyish glow at the zenith and appear bright in the direction of one or more prominent city glows. [-Richard Berry] Some dark lanes in milkyway but no bulge into Ophiuchus. Washed out milkyway visible near horizon. Zodiacal light very rare. Light domes up to 45 degrees. Limiting magnitude about 5.9 to 6.2. [-ad]
4.5     Yellow      (255,250,43)       1.73 - 3.00
5       Dk Red      (190,96,21)        3.00 - 5.20      To a city dweller the M.W. is magnificent, but contrast is markedly reduced, and delicate detail is lost. Limiting magnitude is noticeably reduced. Clouds are bright against the zenith sky. Stars no longer appear large and near. [-Richard Berry] Milkyway washed out at zenith and invisible at horizon. Many light domes. Clouds are brighter than sky. M31 easily visible. Limiting magnitude about 5.6 to 5.9.[-ad]
5       Orange      (233,117,26)       5.20 - 9.00
6       Red         (171,34,14)        9.00 - 15.59     M.W. is marginally visible, and only near the zenith. Sky is bright and discoloured near the horizon in the direction of cities. The sky looks dull grey. [-Richard Berry] Milkyway at best very faint at zenith. M31 difficult and indestinct. Sky is grey up to 35 degrees. Limiting magntidue 5.0 to 5.5. [-ad]
7       Lt Red      (226,46,19)        15.59 - 27.00
8       Dk White    (177,178,177)      27.0 - 46.77     Entire sky is grayish or brighter. Familliar constellations are missing stars. Fainter constellations are absent. Less than 20 stars visible over 30 degrees elevation in brigher areas. Limiting magntude from 3 to 4.CCD imaging is still possible. But telescopic visual observation is usually limited to the moon, planets, double stars and variable stars. [-ad]
9       White       (255,255,255)      47.77+           Stars are weak and washed out, and reduced to a few hundred. The sky is bright and discoloured everywhere. [-Richard Berry] Most people don't look up.[-ad]
"""

pixel_lightpoll_table = {
    '(0, 0, 0)': 0,             # Bortle "0.00 - 0.01",
    '(35, 35, 35)': 0.035,      # Bortle "0.01 - 0.06",
    '(70, 70, 70)': 0.085,      # Bortle "0.06 - 0.11",
    '(0, 0, 153)': 0.15,        # Bortle "0.11 - 0.19",
    '(0, 0, 255)': 0.26,        # Bortle "0.19 - 0.33",
    '(0, 153, 0)': 0.455,       # Bortle "0.33 - 0.58",
    '(0, 255, 0)': 0.79,        # Bortle "0.58 - 1.00",
    '(191, 191, 0)': 1.365,     # Bortle "1.00 - 1.73",
    '(255, 255, 0)': 2.365,     # Bortle "1.73 - 3.00",
    '(217, 109, 0)': 4.1,       # Bortle "3.00 - 5.20",
    '(255, 128, 0)': 7.1,       # Bortle "5.20 - 9.00",
    '(204, 0, 0)': 12.295,      # Bortle "9.00 - 15.59",
    '(255, 0, 0)': 21.295,      # Bortle "15.59 - 27.00",
    '(191, 191, 191)': 36.895,  # Bortle "27.0 - 46.77",
    '(255, 255, 255)': 46.77    # Bortle "46.77+"
}

def inv_gudermannian(y):
    return math.log(math.tan((y + math.pi/2) / 2))


def get_lat_lng_tile(lat, lng, zoom):
    """convert lat/lng to Google-style Mercator tile coordinate (x, y)
    at the given zoom level
    """

    # Reverse mercator distortion for how many degrees a tile covers at different latitudes
    lat_rad = inv_gudermannian(lat * math.pi / 180.0)

    x = 2**zoom * (lng + 180.0) / 360.0
    y = 2**zoom * (math.pi - lat_rad) / (2 * math.pi)

    return (x, y)


def get_light_pollution(lat, lng):
    """Gets the Light Pollution level for the location chosen.

    args: lat/lng for stargazing site
    returns: Double representation of light pollution levels
    """
    curr_dir_path = os.path.dirname(os.path.realpath(__file__))
    tiles_dir_path = os.path.join(curr_dir_path, 'lp_tiles')

    # At zoom 6:
    # 37 Lat Titles, 11-47, -65 to 75 deg, covers 140 deg
    # 64 Lng Tiles: 0-63, -180 to 180 deg, covers 360 deg
    # coverage per tile deppends on latitude & Mercador distortion

    i, j = get_lat_lng_tile(lat, lng, 6)

    # Which tile and how far into it (%) is the pixel?
    i_pixel_percent = i % 1
    j_pixel_percent = j % 1
    pixel_x = i_pixel_percent * 1024
    pixel_y = j_pixel_percent * 1024
    pixel_x = int(max(0, min(pixel_x, 1023))) #prevent out of bounds
    pixel_y = int(max(0, min(pixel_y, 1023)))

    # Floor to consider which tile to look at
    i = int(i)
    j = int(j)

    image_name = "tile_6_%d_%d.png" % (i, j)

    try:
        image_path = os.path.join(tiles_dir_path, image_name)
        # print( "Trying to open image: %s" % image_path #TODO convert to logging)
        image = Image.open(image_path)
        # print( "Looking up pixel ({},{})".format(pixel_x, pixel_y) #TODO convert to logging)
        rgb_img = image.convert("RGB")
        pix = rgb_img.load()
        pixel_value = pix[pixel_x, pixel_y]
        light_poll_ratio = pixel_lightpoll_table[str(pixel_value)]
        # print( image_name, pixel_value, light_poll_ratio)
    except KeyError as e:
        print("Error, color does not match any known in key")
        light_poll_ratio = -1
    except IndexError as e:
        print("Error: %s" % e)
    except IOError as e:
        light_poll_ratio = 0  # If no file exisits/no coverage, almost certainly in very remote area (near poles)
        print("Error: There's no coverage for %s" % image_name)

    return light_poll_ratio  # JsonResponse({'light_pollution': light_poll_ratio})