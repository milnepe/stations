"""Utility modules that return station info by city"""

EMPTY_STRING = ''


def get_cities_list(stations: dict, city: str) -> list:
    """Return list of cities from a stations dict matching city string"""
    cities_list = []
    if city != EMPTY_STRING and city is not None:
        for key in stations:
            if city in key:
                cities_list.append(key)
    return cities_list


def get_station_list(stations: dict, city: str) -> list:
    """Return a list of stations from a station dict matching a valid city"""
    for key in stations[city]:
        if key == 'urls':
            stations_list = stations[city][key]
            return stations_list
    return []


if __name__ == '__main__':
    """
    Search a city and play any matching stations
    eg: python cities.py '../stations.json' 'London'

    https://github.com/oaubert/python-vlc/blob/master/README.module
    """
    import sys
    import pprint
    import logging
    import time
    # import subprocess
    import files
    import python_vlc_streaming
    # import vlc

    stations_file = sys.argv[1]
    city_string = sys.argv[2]

    CLIP_DURATION = 10  # seconds
    audio = 'alsa'

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    stations = files.load_stations(stations_file)
    cities = get_cities_list(stations, city_string)
    if cities:
        pprint.pp(cities)
    else:
        print("Not found")
        exit()

    for city in cities:
        station_list = get_station_list(stations, city)
        print(city)
        pprint.pp(station_list)

        # Now play list
        for station in station_list:
            logging.info(f"Playing URL, {station['name']}, {station['url']}")
            player = python_vlc_streaming.Streamer(audio, station['url'])
            player.play()
            time.sleep(CLIP_DURATION)
            player.stop()

    logging.info("End of list")
