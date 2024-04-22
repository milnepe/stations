"""
Utility that outputs a valid stations file based on a cities name

eg to output the stations file for London UK execute the following commandline:
python stations_by_city_output.py ./json/stations.json London,GB
"""

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
    eg: python stations_by_city_view.py ../json/london-stations.json London,GB

    https://github.com/oaubert/python-vlc/blob/master/README.module
    """
    import sys
    import pprint
    import logging
    import time
    # import subprocess
    from stations.streaming import files
    import python_vlc_streaming
    import json
    # import vlc

    stations_file = sys.argv[1]
    city_string = sys.argv[2]

    CLIP_DURATION = 10  # seconds
    audio = 'alsa'

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    stations = files.load_stations(stations_file)
    city_dict = {}
    for k, v in stations.items():
        if city_string in k:
            city_dict[k] = v
            print(city_dict)

    # Output stations.json file
    with open("out.json", 'w', encoding='utf8') as f:
        json.dump(city_dict, f, indent=2, ensure_ascii=False)

    # cities = get_cities_list(stations, city_string)
    # if cities:
        # pprint.pp(cities)
    # else:
        # print("Not found")
        # exit()

    # for city in cities:
        # print(f"{len(city)} Stations")
        # station_list = get_station_list(stations, city)
        # print(city)
        # pprint.pp(station_list)
