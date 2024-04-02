import pprint
import streaming
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
            stations_list = (stations[city][key])
            return stations_list


if __name__ == '__main__':
    import sys
    import files

    CLIP_DURATION = 10  # seconds

    stations = files.load_stations(sys.argv[1])
    cities = get_cities_list(stations, sys.argv[2])
    if cities:
        pprint.pp(cities)
    else:
        print("Not found")
        exit()
    
    for city in cities:
        station_list = get_station_list(stations, city)
        print(city)
        pprint.pp(station_list)

    for station in station_list:
        station_name = station['name']
        station_url = station['url']
        print(station_name)
        print(station_url)
        # if streaming.check_url(station_url) is not None:
        #     # logging.info("Playing URL, %s, %s", station_name, station_url)
        #     streamer = streaming.Streamer('alsa', station_url)
        #     streamer.play()
        #     time.sleep(CLIP_DURATION)
        #     streamer.stop()
        # else:
        #     # logging.info("Bad URL, %s, %s", station_name, station_url)