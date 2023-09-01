from urllib.parse import urlparse, parse_qs
import re
import os
import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
api_key = os.getenv("api_key_secret")
youtube = build('youtube', 'v3', developerKey=api_key)
def playlists_mismatch_func(playlistlink1, playlistlink2, output='link'):
    """Return the ids of videos that are only one of the playlists, and not in the other"""
    
    def extract_playlist_id(playlistlink):
            match = re.search(r'list=([^&]+)', playlistlink) #It searches for the string 'list=' followed by >=1 characters that are not '&'. 
            if match:
                return match.group(1)
            return None
        
    playlist1id = extract_playlist_id(playlistlink1)
    playlist2id = extract_playlist_id(playlistlink2)
    print("Playlist IDs obtained")

    assert playlist1id!= None, "Playlist 1 link is invalid"
    assert playlist2id!= None, "Playlist 2 link is invalid"

    vid1_ids = []
    vid2_ids = []

    def get_video_ids(playlistid):
        vid_ids = []
        next_page_token = None
        while True:
            pl_request = youtube.playlistItems().list(
                part="contentDetails, snippet",
                playlistId=playlistid,
                maxResults=50,
                pageToken = next_page_token
            )
            pl_response = pl_request.execute()
            for item in pl_response['items']:
                vid_ids.append(item['contentDetails']['videoId'])
                
            next_page_token = pl_response.get('nextPageToken')
            if next_page_token is None:
                break
        return vid_ids

    vid1_ids = get_video_ids(playlist1id)
    print("Playlist 1 video IDs obtained, no. of videos:", len(vid1_ids))
    vid2_ids = get_video_ids(playlist2id)
    print("Playlist 2 video IDs obtained, no. of videos:", len(vid2_ids))

    print("Video IDs obtained")


    def get_playlist_name(playlistid):
        pl_request = youtube.playlists().list(
            part="snippet",
            id=playlistid,
            maxResults=1
        )
        pl_response = pl_request.execute()
        return pl_response['items'][0]['snippet']['title']
    
    playlist1name = get_playlist_name(playlist1id)
    playlist2name = get_playlist_name(playlist2id)



    def get_video_name(videoid):
        vid_request = youtube.videos().list(
            part="snippet",
            id=videoid,
            maxResults=1
        )
        vid_response = vid_request.execute()
        return vid_response['items'][0]['snippet']['title']
    
    firstnotsecond = list(set(vid1_ids) - set(vid2_ids))
    secondnotfirst = list(set(vid2_ids) - set(vid1_ids))
    if output == 'id':
        return firstnotsecond, secondnotfirst, playlist1name, playlist2name
    elif output == 'link':
        firstnotsecond = [f"https://youtu.be/{i}" for i in firstnotsecond]
        secondnotfirst = [f"https://youtu.be/{i}" for i in secondnotfirst]
        return firstnotsecond, secondnotfirst, playlist1name, playlist2name
    elif output == 'name':
        firstnotsecond = [get_video_name(i) for i in firstnotsecond]
        secondnotfirst = [get_video_name(i) for i in secondnotfirst]
        return firstnotsecond, secondnotfirst, playlist1name, playlist2name