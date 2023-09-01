from datetime import timedelta
#from pyyoutube import playlist
import re
import gradio as gr
from urllib.parse import urlparse, parse_qs
from contextlib import suppress
import os

api_key = os.getenv("api_key_secret")
import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
youtube = build('youtube', 'v3', developerKey=api_key)

def get_playlistname_from_link(playlist_link):
    playlist_id = re.search(r'list=(.*)', playlist_link)
    pl_request = youtube.playlistItems().list(
        part="contentDetails,snippet",
        playlistId=playlist_id.group(1),
        maxResults=50
    )
    pl_response= pl_request.execute()
    if 'items' in pl_response:
    playlist = pl_response['items'][0]
    title = playlist['snippet']['title']
    return title

def get_playlistname_from_id(playlist_id):
    playlist_id = playlist_id
    pl_request = youtube.playlistItems().list(
        part="contentDetails,snippet",
        playlistId=playlist_id.group(1),
        maxResults=50
    )
    pl_response= pl_request.execute()
    if 'items' in pl_response:
    playlist = pl_response['items'][0]
    title = playlist['snippet']['title']
    return title

def get_playlistid_from_link(playlist_link):
    match = re.search(r'list=([^&]+)', playlist_link) #It searches for the string 'list=' followed by >=1 characters that are not '&'. 
    if match:
        return match.group(1)
    return None

def extract_playlist_id(playlistlink):
        match = re.search(r'list=([^&]+)', playlistlink) #It searches for the string 'list=' followed by >=1 characters that are not '&'. 
        if match:
            return match.group(1)
        return None

    playlist_id = extract_playlist_id(playlistlink)

    if playlist_id is None:
        return False

    search_request = youtube.playlists().list(

            part='id',
            id=playlist_id,
            maxResults=1
        )
    
    search_response = search_request.execute()
    if 'items' in search_response:
        try:
            playlistdict = search_response['items'][0]
            print("ID of playlist is:- ",playlistdict['id'])
            return playlistdict['id']
        except:
            #print("Video not found.")
            return False




    
    

    