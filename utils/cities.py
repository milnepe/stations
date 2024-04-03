import pprint
import logging
import time


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
    import sys
    import files
    import vlc

    stations_file = sys.argv[1]
    city_string = sys.argv[2]

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    CLIP_DURATION = 10  # seconds

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

        # for station in station_list:
            # station_name = station['name']
            # station_url = station['url']

            # logging.info(f"Playing {station_name}, {station_url}")
            # logging.debug("Starting player...")
            # streamer = vlc.MediaPlayer(station_url)
            # streamer.play()
            # time.sleep(CLIP_DURATION)
            # logging.debug("Stopping player...")
            # streamer.stop()
            # time.sleep(1)
