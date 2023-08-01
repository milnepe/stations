#!/usr/bin/python

"""Stations Json"""

import worldradiomap
import simplemaps
import remove
import json
import stations as st
import stream as s
import time
import remove_href

STATION_LIMIT = 20  # max number of stations per city
# STATION_DATASET = 'https://worldradiomap.com/list'
SIMPLEMAPS_DATASET = 'csv/worldcities-modified.csv'

def run(worldradiomap_json_file, station_json_file):
    '''Generates the stations Json file'''

    # Get the worldradiomap dictionary of URL and index for each city
    # This can be regenerated with worldradiomap.py
    with open(worldradiomap_json_file, "r") as read_file:
        worldradiomap_cities_dict = json.load(read_file)

    # Generate both utf-8 and ascii city dictionaries
    simplemaps_city_dict = simplemaps.city_dict(SIMPLEMAPS_DATASET, 'utf8')
    simplemaps_city_ascii_dict = simplemaps.city_dict(SIMPLEMAPS_DATASET, 'ascii')

    # Match cities
    worldradiomap_city_index = [city for city in worldradiomap_cities_dict]
    simplemaps_city_index = [city for city in simplemaps_city_dict]
    simplemaps_city_ascii_index = [city for city in simplemaps_city_ascii_dict]

    matched_cities = []     # Lists of city indexes that match in worldradio and simplemaps ditcs
    un_matched_cities = []  # All the indexes that don't match
    for city in worldradiomap_city_index:
        if city in simplemaps_city_index:
            matched_cities.append(city)
        else:
            un_matched_cities.append(city)

    for city in un_matched_cities:
        if city in simplemaps_city_ascii_index:
            if city in worldradiomap_city_index:
                if city not in matched_cities:
                    matched_cities.append(city)
                    un_matched_cities.remove(city)

    # Build stations dict based on match
    stations = {}
    error_list = []

    # Add cities to stations dict
    for city in matched_cities:
        stations[city] = {}
        href = worldradiomap_cities_dict[city].get('href')
        stations[city]['href'] = href

        # Add co-ordinates
        if city in simplemaps_city_dict:
            lat = simplemaps_city_dict[city].get('lat')
            lng = simplemaps_city_dict[city].get('lng')
            coords = {}
            coords['n'] = float(lat)
            coords['e'] = float(lng)
            stations[city]['coords'] = coords
        elif city in simplemaps_city_ascii_dict:
            lat = simplemaps_city_ascii_dict[city].get('lat')
            lng = simplemaps_city_ascii_dict[city].get('lng')
            coords = {}
            coords['n'] = float(lat)
            coords['e'] = float(lng)
            stations[city]['coords'] = coords
        else:
            error_list.append(city)

    # Update stations dict with station data for each city
    for city in stations.copy().items():
        urls = {}
        # Retrieve the link to the stations list page
        href = city[1].get('href')
        print(href)
        # Build a dict keyed on station name / link to stream page
        stations_dict = st.stations_dictionary(href)

        # Build list of station name / stream pairs
        stations_list = []
        for idx, s_name in enumerate(stations_dict):
            name = s_name  # usable station name
            print(name)
            # Follow link to stream
            html = stations_dict.get(s_name)
            url = s.station_stream(href, html)  # playable stream
            if url:
                # Add station / stream to list
                stations_list.append({'name': name, 'url': url})
            if idx == STATION_LIMIT:
                break

        stations[city[0]].update({'urls': stations_list})

    # Uouput stations.json file
    with open(station_json_file, 'w', encoding='utf8') as f:
        json.dump(stations, f, indent=2, ensure_ascii=False)

    print('Worldradiomaps Cities Indexed:', len(worldradiomap_cities_dict))
    print('Simplemaps Cities ASCII Indexed: ', len(simplemaps_city_ascii_dict))
    print('Simplemaps Cities UTF-8 Indexed: ', len(simplemaps_city_dict))
    print("Matched cities: ", len(matched_cities))
    print("Un-matched cities: ", len(un_matched_cities))
    print("Stations dictionary indexed: ", len(stations))


if __name__ == '__main__':
    """
    Export stations.json file
    eg: ./main.py 'json/worldradiomap.json' 'json/stations.json'
    """
    import sys

    worldradiomap_json_file = sys.argv[1]
    station_json_file = sys.argv[2]

    #run('csv/test.csv')
    #run('csv/worldcities-modified.csv')
    run(worldradiomap_json_file, station_json_file)

