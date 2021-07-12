"""Stations Dictionary"""

from bs4 import BeautifulSoup
import urllib.request

def stations_dictionary(city_url):
    '''Returns a dictionary of links to station pages indexed by station name for the given city'''

    '''
    Each station page is enclosed in <tr class="rt0">
    The rt0 class are the good ones, there are also rt1 class which are greyed out

    <tr class="rt0">
    <td class="freq">  91.30</td>
    <td class="fsta"><a href="../au/play/sportfm.htm" onclick="Ops(this.href);return false" title="Listen live">
    <img class="station" src="../au/images/sportfm.gif"/> 6WSM Sport FM
        <img align="absmiddle" height="21" src="../2013/images/icon.gif" width="16"/></a></td>
    <td class="fpre">East Fremantle</td>
    </tr>
    '''

    stations = dict()

    req = urllib.request.Request(url=city_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as html:
            soup = BeautifulSoup(html, 'html.parser')

        # Build dict of station links indexed by station name
        # Some hrefs point to non-worldradio pages so these are removed
        # tr_soup = soup.find_all("tr", class_="rt0")
        for tr in soup.find_all("tr", class_="rt0"):
            name = None
            name_tag = tr.find('a', href=True)
            if name_tag:
                name = name_tag.text.strip()

                ref = None
                href = name_tag['href']
                # We only want links to worldradiomap not local site ones
                if href.startswith('../'):
                    ref = href.replace('..', '')

                if name not in stations:
                    stations[name] = ref

        # Now remove entries with empty values
        stations = {k: v for k, v in stations.items() if v}

    except:
        print('Request failed')

    return stations


if __name__ == '__main__':
    import sys
    # stations_dictionary(http://radiomap.eu/no/oslo.htm)
    stations_dict = stations_dictionary(sys.argv[1])
    print(stations_dict)

    # stations_dict = stations_dictionary('http://worldradiomap.com/uk/london.htm')
    # stations_dict = stations_dictionary('http://worldradiomap.com/au/perth.htm')
    # print(stations_dict)
    # for k, v in stations_dict.items():
        # print(k, v)
