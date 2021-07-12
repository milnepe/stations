'''Remove cities with empty key values

Removes cities from the city dict were specified key values are empty

Example: remove cities with no coordinates
python3 remove.py stations.json 'coords' removed.json
'''

import json


def remove_city(city_dict, empty_key, removed_json):
    '''Remove cities from dictionary that have no coordinates'''

    cities_indexed = len(city_dict)

    pop_list = list()
    found = 0
    for city in city_dict:
        c = city_dict.get(city)
        coords = c.get(empty_key)
        if not coords:
            found += 1
            pop_list.append(city)

    for city in pop_list:
        city_dict.pop(city)

    print('Removed Cities Indexed:', cities_indexed)
    print('Removed Cities Removed:', found)
    print('Removed Dataset:', removed_json)

    with open(removed_json, 'w', encoding='utf8') as f:
        json.dump(pop_list, f, ensure_ascii=False)


if __name__ == '__main__':
    import sys

    with open(sys.argv[1], 'r') as f:
        city_dict = json.load(f)

    remove_city(city_dict, 'coords', sys.argv[2])
