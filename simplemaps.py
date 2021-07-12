'''Simplemaps Dictionary

Generates Python dictionaries containing city data from simplemaps csv
Output can also be extracted as json by running scrip

Provides 2 city dictionaries:
city_dict() - City data indexed by UTF-8 city name
city_ascii_dict() - City data indexed by ascii name


Test dataset - source simplemaps.com

"city","city_ascii","lat","lng","country","iso2","iso3","admin_name","capital","population","id"
"Tokyo","Tokyo","35.6897","139.6922","Japan","JP","JPN","Tōkyō","primary","37977000","1392685764"
"Jakarta","Jakarta","-6.2146","106.8451","Indonesia","ID","IDN","Jakarta","primary","34540000","1360771077"
"Delhi","Delhi","28.6600","77.2300","India","IN","IND","Delhi","admin","29617000","1356872604"
"Mumbai","Mumbai","18.9667","72.8333","India","IN","IND","Mahārāshtra","admin","23355000","1356226629"
"Manila","Manila","14.5958","120.9772","Philippines","PH","PHL","Manila","primary","23088000","1608618140"
"Shanghai","Shanghai","31.1667","121.4667","China","CN","CHN","Shanghai","admin","22120000","1156073548"
"New York","New York","40.6943","-73.9249","United States","US","USA","New York","","18713220","1840034016"
"Kolkāta","Kolkata","22.5411","88.3378","India","IN","IND","West Bengal","admin","17560000","1356060520"
"London","London","51.5072","-0.1275","United Kingdom","GB","GBR","London, City of","primary","10979000","1826645935"
"İstanbul","Istanbul","41.0100","28.9603","Turkey","TR","TUR","İstanbul","admin","15154000","1792756324"
"Sofia","Sofia","42.6975","23.3241","Bulgaria","BG","BGR","Sofia-Grad","primary","1355142","1100762037"
"La La","La La","0.1","0.01","La L Land","LL","LLL","La La","primary","2","0"

Usage:
python3 simplemaps.py
'''
import csv
import states
import json

# Get a dict of US state name / codes
states = states.states_dictionary()


def add_city(cities, city, row):
    '''Adds a city to cities dictionary'''

    cities[city] = {}
    cities[city]['city_ascii'] = row['city_ascii']
    cities[city]['lat'] = row['lat']
    cities[city]['lng'] = row['lng']
    cities[city]['country'] = row['country']
    cities[city]['iso2'] = row['iso2']
    cities[city]['iso3'] = row['iso3']
    cities[city]['admin_name'] = row['admin_name']
    cities[city]['capital'] = row['capital']
    cities[city]['population'] = row['population']
    cities[city]['id'] = row['id']


def city_dict(map_csv):
    '''Simple map dictionary indexed on city'''

    cities = dict()
    counter = 0
    with open(map_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Map 'country' onto city name
            # For US cities we want the form 'New York,US-NY'
            # so we need to lookup the admin name in the states dict
            counter += 1
            if row['iso2'] == 'US':
                admin_name = row['admin_name']
                city = row['city'] + ',' + states.get(admin_name)
            else:
                city = row['city'] + ',' + row['iso2']

            add_city(cities, city, row)

    print('Simplemaps Cities UTF-8: Indexed', counter)
    return cities


def city_ascii_dict(map_csv):
    '''Simple map dictionary indexed on city'''

    cities = dict()
    counter = 0
    with open(map_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Map 'country' onto city name
            # For US cities we want the form 'New York,US-NY'
            # so we need to lookup the admin name in the states dict
            counter += 1
            if row['iso2'] == 'US':
                admin_name = row['admin_name']
                city = row['city'] + ',' + states.get(admin_name)
            else:
                city = row['city_ascii'] + ',' + row['iso2']

            add_city(cities, city, row)

    print('Simplemaps Cities ASCII: Indexed', counter)
    return cities


if __name__ == '__main__':
    city = city_dict('test.csv')

    with open('simplemaps.json', 'w', encoding='utf8') as f:
        json.dump(city, f, ensure_ascii=False)

    city_ascii = city_ascii_dict('test.csv')

    with open('simplemaps_ascii.json', 'w', encoding='utf8') as f:
        json.dump(city_ascii, f, ensure_ascii=False)
