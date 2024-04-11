# Thanks to Peter Milne!
import time
import subprocess
import os
import signal
from pathlib import Path
import json
import re
import requests
from requests.exceptions import Timeout
import concurrent.futures
import logging
import random
import files

# mixer_name = None


# def launch(audio: str, url: str) -> int:
    # """Play url returning the vlc pid"""
    # logging.debug("Launching audio: %s, %s", audio, url)
    # radio = subprocess.Popen(['cvlc', '--aout', audio, url])
    # return radio.pid


# class Streamer ():
    # """A streaming audio player using vlc's command line"""

    # def __init__(self, audio, url):
        # logging.debug("Starting Streamer: %s, %s", audio, url)
        # self.audio = audio
        # self.url = url
        # self.radio_pid = None

    # def play(self):
        # with concurrent.futures.ProcessPoolExecutor() as executor:
            # try:
                # # Play streamer in a separate process
                # ex = executor.submit(launch, self.audio, self.url)
                # logging.debug("Pool Executor: %s, %s", self.audio, self.url)
            # except Exception as e:
                # logging.debug("Pool Executor error: %s", e)
            # else:
                # # Get the vlc process pid so it can be stopped (killed!)
                # self.radio_pid = ex.result()
                # logging.debug("Pool Executor PID: %s", self.radio_pid)

    # def stop(self):
        # """Kill the vlc process. It's a bit brutal but it works
        # even for streams that send vlc into a race condition,
        # which is probably a bug in vlc"""
        # try:
            # os.kill(self.radio_pid, signal.SIGKILL)
            # logging.debug("Killing Streamer PID: %s", self.radio_pid)
        # except Exception as e:
            # logging.debug("Kill Streamer error: %s", e)


if __name__ == "__main__":
    import sys
    import vlc
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    clip_duration = 10

    stations_file = sys.argv[1]
    stations = files.load_stations(stations_file)

    # Get list of stations
    station_list = []
    for k, v in stations.items():
        for v in v['urls']:
            station_list.append(v)

    logging.debug(station_list)
    logging.info(f"Station list length: {len(station_list)} URLs")

    # Play each station for a few seconds
    playlists = set(['pls', 'm3u'])
    Instance = vlc.Instance()

    for i, station in enumerate(station_list):
        url = station['url'].strip()
        logging.info(f"Playing URL {i}, {station['name']}, {url}")

        # We need a different type of media instance for urls containing playlists
        extension = (url.rpartition(".")[2])[:3]
        logging.debug(f"Extension: {extension}")
        if extension in playlists:
            logging.debug(f"Creating media_list_player...")
            player = Instance.media_list_player_new()
            media = Instance.media_list_new([url])
            player.set_media_list(media)
        else:
            logging.debug(f"Creating media_player...")
            player = Instance.media_player_new()
            media = Instance.media_new(url)
            player.set_media(media)

        player.play()
        time.sleep(clip_duration)
        player.stop()

    logging.info("End of list")
