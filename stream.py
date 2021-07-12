"""Station Stream Lib"""

from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin


def station_stream(href, rel_url):
    '''Returns a playable stream url from a given station page and relative url'''

    '''
    Each station link is contained in a <div> tag with playlist id
    <div id="playlist">
    <a href="http://streamer5.rightclickitservices.com:7200/listen.pls" target=_self>
        <u>聆听您的播放器</u>
        <img src="../../2013/images/icon.gif" width=16 height=21 align=absmiddle alt="聆听您的播放器">
    </a>
    </div>
    '''

    stream = None
    station_url = urljoin(href, rel_url)
    try:
        req = urllib.request.Request(url=station_url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req, timeout=5) as html:
            soup = BeautifulSoup(html, 'html.parser')

            playlist_soup = soup.find('div', id='playlist')
            if playlist_soup:
                stream = playlist_soup.find('a', href=True)['href']
                # Clean-up dodgy urls
                stream = stream.replace('/;', '')
    except:
        print('Request failed')

    return stream


if __name__ == '__main__':
    import sys
    # stream = station_stream('http://worldradiomap.com', '/au/play/perth905.htm')
    stream = station_stream(sys.argv[1], sys.argv[2])
    print(stream)
