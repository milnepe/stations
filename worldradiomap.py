#!/usr/bin/python

"""
Worldradiomap Dictionary

Parses World Radio Map list and returns a dictionary of cities with their corresponding
URL index.

city_stations_dict() takes an optional parameter containing a country string or list of countries can be used as a filter.
eg:
cities_dict = city_stations_dict('GB')  # Index UK cities
cities_dict = city_stations_dict(['GB', 'US-CA'])  # Index UK & Californian cities
cities_dict = city_stations_dict()  # Index all cities

Usage: python worldradiomap.py
"""

import requests
import json
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse
import sys

DATASET = 'https://worldradiomap.com/list'


def has_ref_but_no_title(tag):
    """Return the aref we want to parse"""
    return tag.has_attr('href') and not tag.has_attr('title') and not tag.has_attr('class')


def city_stations_dict(countries=None):
    '''Returns a dictionary of pages containing links to local radio stations indexed by city'''

    # The full index contains ~1100 major cities
    #
    # Keys are a combination of city name appended with its ISO 3166 country code since several cities have identical names.
    #
    # Country codes are extracted from the first element of the URL path and converted to upper case, for example:
    # <a href="https://worldradiomap.com/us-ca/san-francisco.htm">San Francisco, CA</a>
    # results in a city index of 'San Francisco,US-CA'
    #
    # Some country codes are modified so the match ISO 3166:
    # UK is changed to GB (ISO 3166)
    #
    # The modified country code is appended to the city to form the index:
    # 'Mumbi,IN' or in the US, 'New York,US-NY'

    cities = {}
    req = urllib.request.Request(url=DATASET, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as html:
            soup = BeautifulSoup(html, 'html.parser')
    except Exception as error:
        print(error)

    for a in soup.find_all(has_ref_but_no_title):
        href = a['href']
        city = a.text
        if not city.strip():
            continue
        if city == "World Radio Map":
            continue

        # Extract country element from url path [0] is backslash, [1] is country
        country = urlparse(href).path.split('/')[1].upper()
        # Change UK to GB
        if country == 'UK':
            country = 'GB'

        city = city.split(',', 1)
        city = city[0] + ',' + country

        if countries:
            if country in countries:
                # create dict
                cities[city] = {}
                cities[city]['href'] = href
        else:
            print(city)
            cities[city] = {}
            cities[city]['href'] = href

    return cities


if __name__ == '__main__':
    """Generate json representation of cities dictionary"""
    cities_dict = {}
    try:
        # Pass in comma separated list of counties eg ./worldradiomap.py 'GB,US-CA'
        countries = sys.argv[1].split(sep=",")
        cities_dict = city_stations_dict(countries)
    except IndexError:
        # Index all eg ./worldradiomap.py
        cities_dict = city_stations_dict()

    with open('json/worldradiomap.json', 'w', encoding='utf8') as f:
        json.dump(cities_dict, f, indent=2, ensure_ascii=False)

    print('Worldradiomaps Dataset:', DATASET)
    print('Worldradiomaps Cities Indexed:', len(cities_dict))
