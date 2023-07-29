#!/usr/bin/python
""" Filter a list of cities in simplemaps format

    Usage: filter_cities.py <population> <input_file.csv> <output_file.csv>
    Cities over 1M:
    ./filter_cities.py 1000000 'worldcities.csv' 'cities.csv'
"""

import sys
import csv

population = int(sys.argv[1])
input_csv = sys.argv[2]
output_csv = sys.argv[3]

filtered_list = []


def filter_cities(population: int, input_csv: str) -> list:
    with open(input_csv, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            try:
                if int(row[9]) > population:
                    filtered_list.append(row)
            except ValueError:
                pass
    return filtered_list


def output_cities(filtered_list, output_csv: str) -> int:
    with open(output_csv, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        for row in filtered_list:
            spamwriter.writerow(row)
    return len(filtered_list)


if __name__ == "__main__":
    cities = filter_cities(population, input_csv)
    number_of_cities = output_cities(cities, output_csv)
    print("Number of cities: ", number_of_cities)
