'''Simplemaps Filter

Filters a "simplemaps.csv" file to output file based on a list filter for a column

For example you can filter out a file containing just capital cities:

python3 filter.py

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

'''
import csv


def cities_filter(input_csv, output_csv, filter_list, match_column):
    '''Generates Simplemaps csv filtered by input list for the match column (zero idx) of input'''

    CITIES_DATASET = input_csv
    CAPITALS_DATASET = output_csv

    index = 0
    counter = 0
    with open(CITIES_DATASET, newline='') as fin, open(CAPITALS_DATASET, 'w', newline='') as fout:
        writer = csv.writer(fout, quoting=csv.QUOTE_ALL)
        writer.writerow(["city", "city_ascii", "lat", "lng", "country", "iso2", "iso3", "admin_name", "capital", "population", "id"])
        for row in csv.reader(fin):
            index += 1
            if row[match_column] in filter_list:
                writer.writerow(row)
                counter += 1

    print('Simplemaps Cities Dataset:', CITIES_DATASET)
    print('Simplemaps Capitals Dataset:', CAPITALS_DATASET)
    print('Simplemaps Cities Indexed:', index)
    print('Simplemaps Capitals Added:', counter)


if __name__ == '__main__':
    # Capital index is column 8, 'primary'
    capitals_list = ['primary']
    cities_filter('simplemaps.csv', 'capitals.csv', capitals_list, 8)
