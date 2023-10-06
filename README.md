---
title: Youtube Playlist
emoji: 🎥
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 3.35.2
app_file: app.py
pinned: false
license: cc
---
# Total duration of playlist
For a given playlist, it calculates the duration of each public video in that playlist and sums them to produce the total duration. The total duration of the playlist given below is 1 hour, 58 minutes.
[Playlist link](https://youtube.com/playlist?list=PLuhqtP7jdD8CD6rOWy20INGM44kULvrHu&si=G4rrT1wQfQVvzTJF)

<p align="center">
  <img src="images/total_duration.png" alt="CloudSat orbit superimposed on INSAT-3DR coverage area.">
</p>


# Average duration of a playlist
Average duration of videos is calculated for the publicly available videos in that playlist. For example, the average duration of videos in this playlist is around 9 minutes.

<p align="center">
  <img src="images/average_duraiton.png" alt="CloudSat orbit superimposed on INSAT-3DR coverage area.">
</p>


# Playlist mismatch
Given two playlists, this function gets the videos that are present in one of the playlists, but not in the other. 
The two playlists are given here, [HindiSongs1](https://youtube.com/playlist?list=PLgeEuUJpv5I-jRo3Ibddg96Ke5QRryBQf&si=HZKtxDOm6RbmYieu) and [HindiSongs2](https://youtube.com/playlist?list=PLgeEuUJpv5I-0eV03cUzMAVyHDyVV_43D&si=t8mf-O0CNe23dwlS).
<p align="center">
  <img src="images/mismatch.png" alt="CloudSat orbit superimposed on INSAT-3DR coverage area.">
</p>









**************************************************************************************************
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
