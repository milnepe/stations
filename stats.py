"""Station Stats

Report cities and stations sorted by country

Usage:
python3 stats.py stations.json report.csv
"""

import json
from collections import Counter


def run(station_dataset, summary_file):
    '''Generates statistics'''

    with open(station_dataset, 'r', encoding='utf8') as f:
        cities = json.load(f)

    print('Station Dataset:', station_dataset)
    print('Total Cities:', len(cities))

    count = sum([len(cities[x]['urls']) for x in cities if isinstance(cities[x]['urls'], list)])
    print('Total Stations:', count)

    summary_list = list()
    for c, items in cities.items():
        city, country = c.split(',')
        summary = [country, city, len(items['urls'])]
        summary_list.append(summary)
    summary_list.sort()

    with open(summary_file, 'w', encoding='utf8') as f:
        for s in summary_list:
            f.write(s[1] + ',' + s[0] + ',' + str(s[2]) + '\n')


if __name__ == '__main__':
    """python stats.py json/stations.json json/stats.csv"""
    import sys
    run(sys.argv[1], sys.argv[2])
