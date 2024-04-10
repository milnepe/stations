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
    # # logging.getLogger().setLevel(logging.DEBUG)

    stations_file = sys.argv[1]
    clip_duration = 10

    playlists = set(['pls', 'm3u'])

    stations = files.load_stations(stations_file)

    # Get list of urls
    url_list = [url['url'].strip() for k, v in stations.items() for url in v['urls']]
    urls = list(set(url_list))  # De-duped list
    logging.info("Station list length: %s, URLs", len(urls))

    Instance = vlc.Instance()

    while True:
        # i = random.choice(range(len(urls)))
        # url = urls[i]
        for url in urls:
            logging.info("Playing URL, %s", url)

            playlists = set(['pls', 'm3u'])

            ext = (url.rpartition(".")[2])[:3]
            test_pass = False

            print(f'Sampling for {clip_duration} seconds')
            player = Instance.media_player_new()
            Media = Instance.media_new(url)
            Media_list = Instance.media_list_new([url])
            Media.get_mrl()
            player.set_media(Media)
            if ext in playlists:
                list_player = Instance.media_list_player_new()
                list_player.set_media_list(Media_list)
                if list_player.play() == -1:
                    print("Error playing playlist")
            else:
                if player.play() == -1:
                    print("Error playing Stream")
            time.sleep(clip_duration)
            if ext in playlists:
                list_player.stop()
            else:
                player.stop()
