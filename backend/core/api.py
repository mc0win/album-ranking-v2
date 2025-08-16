import spotipy
import discogs_client
import re
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


load_dotenv()
d = discogs_client.Client("album-ranking/1.0")
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def processSpotify(url: str):
    album = sp.album(url)
    tracklist = {}
    tracklist["artist"] = album["artists"][0]["name"]
    tracklist["name"] = album["name"]
    tracklist["release_year"] = int(album["release_date"][:4])
    for track in album["tracks"]["items"]:
        tracklist[track["track_number"]] = track["name"]
    return tracklist


def processDiscogs(source: str, url: str):
    tracklist = {}
    id = re.findall(r"\/(\d+)", url)[0]
    if source == "discogs-master":
        album = d.master(id)
    else:
        album = d.release(id)
    tracklist["artist"] = album.artists[0].name
    tracklist["name"] = album.title
    tracklist["release_year"] = album.year
    i = 1
    for track in album.tracklist:
        tracklist[i] = track.title
        i += 1
    return tracklist


def processUrl(source: str, url: str):
    if "discogs" in source:
        return processDiscogs(source, url)
    return processSpotify(url)
