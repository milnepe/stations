
"""
Remove stations based on list of station names

Generates a new stations file which is a copy of the original with the stations removed.

Usage: update_stations <stations_json> <new_stations_json>
eg: python update_stations.py json/stations.json json/london-stations.json

"""

import json
import files


def run(stations_json, new_stations_json, city, station_names_list):

    # Get stations dict
    stations = files.load_stations(stations_json)
    try:
        stations_list = stations[city]['urls']
    except Exception:
        print("Check args...")
        exit()

    new_stations_list = []
    for station in stations_list:
        if station['name'] not in station_names_list:
            new_stations_list.append(station)

    stations[city]['urls'] = new_stations_list
    print(stations)

    with open(new_stations_json, 'w', encoding='utf8') as f:
        json.dump(stations, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # python remove_stations.py ../json/london-stations.json ../json/new-stations.json 'London,GB' 'BBC Radio 2, Radio Pete'
    import sys

    stations_json = sys.argv[1]
    new_stations_json = sys.argv[2]
    city = sys.argv[3]
    station_names_list = sys.argv[4].split(",")

    run(stations_json, new_stations_json, city, station_names_list)
