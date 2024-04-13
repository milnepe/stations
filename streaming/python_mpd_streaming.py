"""
    Wrapper class for Python MPD client
    Requires MPD
    and pip install python-mpd2
    
    Note: This seems to have problems playing some stations for example
        "name": "Capital (London)",
        "url": "https://media-ice.musicradio.com/CapitalMP3.m3u"
    and
        "name": "Flex FM",
        "url": "http://142.4.215.64:8116/listen.pls?sid=1"
    and
        "name": "NuSound Radio",
        "url": "http://icecast.commedia.org.uk:8000/nusound.mp3.m3u"
        This can be fixed by removing the end .m3u extension

    So python_vlc_streamer.py is prefered at the moment
"""
import time
import logging
import files
from mpd import MPDClient


class Streamer():
    def __init__(self, audio, url):
        logging.debug(f"Starting Streamer: {audio}, {url}")
        self.audio = audio
        self.url = url
        self.player = None

        self.player = MPDClient()
        self.player.timeout = 10
        self.player.idletimeout = None
        self.player.connect("localhost", 6600)

        # url = self.url.strip()
        logging.debug(f"Playing URL {url}")

    def play(self, url):
        self.player.add(url.strip())
        self.player.play()

    def stop(self):
        self.player.stop()
        self.player.clear()


if __name__ == "__main__":
    """python python_mpd_streaming.py ../json/test.json"""
    import sys

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    clip_duration = 10
    audio = 'alsa'

    stations_file = sys.argv[1]
    stations = files.load_stations(stations_file)

    # Get list of stations
    station_list = []
    for k, v in stations.items():
        for v in v['urls']:
            station_list.append(v)

    logging.debug(station_list)
    logging.info(f"Station list length: {len(station_list)} URLs")

    player = Streamer(audio, None)
    for i, station in enumerate(station_list):
        url = station['url']
        logging.info(f"Playing URL {i}, {station['name']}, {url}")
        player.play(url)
        time.sleep(clip_duration)
        player.stop()

    logging.info("End of list")
