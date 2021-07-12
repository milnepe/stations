'''Remove hrefs

Removes cities from the dict with empty hrefs

Usage:
pthone3 remove_href.py stations.json removed.json
'''

import json


def remove_href(city_dict):
    '''Remove cities from dictionary that have no coordinates'''

    cities_indexed = len(city_dict)

    found = 0
    for city in city_dict.copy().items():
        d = city[1]
        if isinstance(d, dict):
            found += 1
            d.pop('href', None)

    print('Removed Cities Indexed:', cities_indexed)
    print('Removed Hrefs Removed:', found)


if __name__ == '__main__':
    import sys

    with open(sys.argv[1], 'r') as f:
        city_dict = json.load(f)

    remove_href(city_dict, sys.argv[2])

    with open(sys.argv[2], 'w', encoding='utf8') as f:
        json.dump(city_dict, f, ensure_ascii=False)
