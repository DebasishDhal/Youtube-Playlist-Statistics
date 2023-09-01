#import pyyoutube
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

def playlist_average_duration_func(youtubelink,videoid=False):

    def playlist_exist_check(playlistlink):

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

    playlistid = playlist_exist_check(youtubelink)
    if playlistid == False or playlistid==None:
        print("Playlist doesn't exist")
        return False
    print("1st check passed - Playlist link is valid")  




#This section retrieves the video ids of all the videos in the playlist, and stores them in a list. 50 in one iteration.

    vid_ids = []
    next_page_token = None
    while True:


        pl_request = youtube.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=playlistid,
            maxResults=50, #This is the max limit of videos that can be fetched in one go form a playlist as youtube data v3 API results are paginated
            pageToken=next_page_token
            )
        pl_response = pl_request.execute()
        # print("Reponse obtained from youtube")


        
        for item in pl_response['items']:
            vid_id = item['contentDetails']['videoId']
            vid_ids.append(vid_id)
            if videoid==True:
                print(item['contentDetails']['videoId'])    

        next_page_token = pl_response.get("nextPageToken")
        if not next_page_token:
            break
    print("2nd check passed - Playlist read")



#This section obtains the playlist name from the playlist id
    pl_request = youtube.playlists().list(
        part="snippet",
        id=playlistid,
        maxResults=1
        )
    pl_response = pl_request.execute()
    playlist = pl_response['items'][0]
    title = playlist['snippet']['title']
    print("Playlist Title:", title)






    # title = playlist['snippet']['title']
    # print("Playlist Title:", title)
#This section retrieves the duration of each video in the playlist, and stores them in a list. 50 in one iteration


    iterations = len(vid_ids)//50+1
    duration_list = []
    for i in range(iterations):
        start_index = i * 50
        end_index = (i + 1) * 50
        batch_ids = vid_ids[start_index:end_index]
        vid_request = youtube.videos().list(
            part="contentDetails",
            id=','.join(batch_ids)
        )

        vid_response = vid_request.execute()


        for item in vid_response['items']:
            duration = item['contentDetails']['duration']
            duration = duration[2:]
            hours = 0
            minutes = 0
            seconds = 0

            if "H" in duration:
                hours_index = duration.index("H")
                hours = int(duration[:hours_index])
                duration = duration[hours_index+1:]

            if "M" in duration:
                minutes_index = duration.index("M")
                minutes = int(duration[:minutes_index])
                duration = duration[minutes_index+1:]

            if "S" in duration:
                seconds_index = duration.index("S")
                seconds = int(duration[:seconds_index])           

            duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            duration_list.append(duration)
    print("3rd check passed - Individual video duration calculated")
    total_duration = sum(duration_list, timedelta())
    #Find the average duration of each video in the playlist
    average_duration = total_duration/len(vid_ids)
    print("Total duration of playlist is:- ",total_duration)
    print("Total no. of videos is = ",len(vid_ids))
    print("Average duration of each video is:- ",average_duration)
    #Convert the average suration into HH:MM:SS format
    # average_duration_format = s
    return str(average_duration)

