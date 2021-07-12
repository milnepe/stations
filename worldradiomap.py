"""Worldradiomap Dictionary"""

import requests
import json
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse


def has_ref_but_no_title(tag):
    return tag.has_attr('href') and not tag.has_attr('title') and not tag.has_attr('class')


def city_stations_dict(dataset):
    '''Returns a dictionary of pages containing links to local radio stations indexed by city'''

    # ~1100 major cities are indexed
    # Keys are a combination of city name appended with its ISO 3166 country code since
    # several cities have identical names
    # Country codes are extracted from the first element of the URL path for example:
    # 'Mumbi,IN' or in the US, 'New York,US-NY'.
    # UK is changed to GB (ISO 3166)

    cities = {}
    counter = 0
    req = urllib.request.Request(url=dataset, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as html:
            soup = BeautifulSoup(html, 'html.parser')
    except:
        print('Request failed')

    for a in soup.find_all(has_ref_but_no_title):
        href = a['href']
        city = a.text

        # Extract country element from url path [0] is backslash, [1] is country
        country = urlparse(href).path.split('/')[1].upper()
        # Change UK to GB
        if country == 'UK':
            country = 'GB'

        city = city.split(',', 1)
        city = city[0] + ',' + country

        # create dict
        cities[city] = {}
        cities[city]['href'] = href
        counter += 1

    print('Worldradiomaps Dataset:', dataset)
    print('Worldradiomaps Cities Indexed:', counter)

    return cities


if __name__ == '__main__':
    cities_dict = city_stations_dict('https://worldradiomap.com/list')

    with open('worldradiomap.json', 'w', encoding='utf8') as f:
        json.dump(cities_dict, f, ensure_ascii=False)
