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

STATION_DATASET = 'https://worldradiomap.com/list'

REMOVED_NO_COORDS = 'removed_no_coords.json'

REMOVED_NO_STATIONS = 'removed_no_stations.json'


def run(city_dataset, output_dataset):
    '''Generates the stations Json file'''

    # Generate city stations dict - lookup for stations
    cities = worldradiomap.city_stations_dict(STATION_DATASET)

    # Generate both utf-8 and ascii key maps - lookup for lat, lng, etc..
    city_dict = simplemaps.city_dict(city_dataset)
    city_ascii_dict = simplemaps.city_ascii_dict(city_dataset)

    stations = dict()
    error_list = list()

    cities_indexed = 0
    errors = 0

    # Add city to dict
    for city in cities:
        stations[city] = {}
        href = cities[city].get('href')
        stations[city]['href'] = href
        cities_indexed += 1

        if city in city_dict:
            lat = city_dict[city].get('lat')
            lng = city_dict[city].get('lng')
            coords = {}
            coords['n'] = float(lat)
            coords['e'] = float(lng)
            stations[city]['coords'] = coords
        elif city in city_ascii_dict:
            lat = city_ascii_dict[city].get('lat')
            lng = city_ascii_dict[city].get('lng')
            coords = {}
            coords['n'] = float(lat)
            coords['e'] = float(lng)
            stations[city]['coords'] = coords
        else:
            error_list.append(city)
            errors += 1

    # For debugging
    with open('worldradiomap.json', 'w', encoding='utf8') as f:
        json.dump(stations, f, ensure_ascii=False)

    # Remove cities with no coords
    remove.remove_city(stations, 'coords', REMOVED_NO_COORDS)

    # Update stations dict with station data for each city
    for city in stations.copy().items():
        urls = dict()
        # Retrieve the link to the stations list page
        href = city[1].get('href')
        print(href)
        # time.sleep(1)
        # Build a dict keyed on station name / link to stream page
        stations_dict = st.stations_dictionary(href)

        # Build list of station name / stream pairs
        limit = STATION_LIMIT
        stations_list = list()
        for idx, s_name in enumerate(stations_dict):
            name = s_name  # usable station name
            print(name)
            # Follow link to stream
            html = stations_dict.get(s_name)
            url = s.station_stream(href, html)  # playable stream
            if url:
                # Add station / stream to list
                stations_list.append({'name': name, 'url': url})
            if idx == limit:
                break

        stations[city[0]].update({'urls': stations_list})

    # Remove cities with no stations urls
    remove.remove_city(stations, 'urls', REMOVED_NO_STATIONS)

    # Remove city hrefs
    remove_href.remove_href(stations)

    print('Main Station Dataset:', STATION_DATASET)
    print('Main City Dataset:', city_dataset)
    print('Main Output Dataset:', output_dataset)
    print('Main Cities:', len(city_dict))
    print('Main Cities Not Matched:', errors)
    print('Main Cities Indexed:', len(stations))

    with open(output_dataset, 'w', encoding='utf8') as f:
        json.dump(stations, f, ensure_ascii=False)

    with open('errors.json', 'w', encoding='utf8') as f:
        json.dump(error_list, f, ensure_ascii=False)


if __name__ == '__main__':
    import sys
    # run(<'city_dataset.csv'>, <'output.json'>)
    run(sys.argv[1], sys.argv[2])
