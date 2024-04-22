"""Utility module to play station by city"""

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
    eg: python stations_by_city_play.py ../json/stations.json London,GB

    https://github.com/oaubert/python-vlc/blob/master/README.module
    """
    import sys
    import pprint
    import logging
    import time
    # import subprocess
    import files
    from python_vlc_streaming import Streamer
    # import vlc

    stations_file = sys.argv[1]
    city_string = sys.argv[2]

    CLIP_DURATION = 10  # seconds

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    stations = files.load_stations(stations_file)
    cities = get_cities_list(stations, city_string)
    if cities:
        pprint.pp(cities)
    else:
        print("Not found")
        exit()

    for city in cities:
        print(f"{len(city)} Stations")
        station_list = get_station_list(stations, city)
        print(city)
        pprint.pp(station_list)

        # Now play list
        player = Streamer()
        for station in station_list:
            url = station['url']
            logging.info(f"Playing URL, {station['name']}, {url}")
            player.play(url)
            time.sleep(CLIP_DURATION)

    logging.info("End of list")
