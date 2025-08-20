import spotipy
import discogs_client
import re
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
import datetime

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
USER_TOKEN = os.getenv("USER_TOKEN")

d = discogs_client.Client(
    "album-ranking/1.0",
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    user_token=USER_TOKEN,
)
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def processSpotify(url: str):
    album = sp.album(url)
    tracklist = {}
    tracklist["artist"] = album["artists"][0]["name"]
    tracklist["name"] = album["name"]
    tracklist["release_year"] = int(album["release_date"][:4])
    tracklist["total_tracks"] = album["total_tracks"]
    tracklist["cover"] = album["images"][0]["url"]
    duration = 0
    for track in album["tracks"]["items"]:
        tracklist[track["track_number"]] = track["name"]
        duration += track["duration_ms"]
    tracklist["duration"] = (
        datetime.datetime.min + datetime.timedelta(seconds=duration // 1000)
    ).time()
    return tracklist


def processDiscogs(source: str, url: str):
    tracklist = {}
    id = re.findall(r"\/(\d+)", url)[0]
    album = d.master(id)
    tracklist["artist"] = album.main_release.artists[0].name
    tracklist["name"] = album.title
    tracklist["release_year"] = album.year
    tracklist["total_tracks"] = len(album.tracklist)
    tracklist["cover"] = album.main_release.images[0]["resource_url"]
    i = 1
    duration = 0
    for track in album.tracklist:
        if len(track.duration) != 0:
            time = track.duration.split(":")
            duration += int(time[0]) * 60 + int(time[1])
            tracklist[i] = track.title
            i += 1
    tracklist["duration"] = (
        datetime.datetime.min + datetime.timedelta(seconds=duration)
    ).time()
    return tracklist


def processUrl(source: str, url: str):
    if "discogs" in source:
        return processDiscogs(source, url)
    return processSpotify(url)