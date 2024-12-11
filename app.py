import gradio as gr
import urllib
from urllib.parse import urlparse, parse_qs

from playlist_duration import playlist_duration_func
from average_duration import playlist_average_duration_func
from playlists_mismatch import playlists_mismatch_func

def playlist_duration_calculator(playlist_link, calculation_type):
    if calculation_type == "Total Duration":
        result = playlist_duration_func(playlist_link)
        return f"Total Duration: {result}"
    elif calculation_type == "Average Duration":
        result = playlist_average_duration_func(playlist_link)
        return f"Average Duration: {result}"

heading = "YouTube Playlist Duration Calculator"
description = '''Enter a YouTube playlist link to calculate its total duration or average duration.\n
Do not enter the link of a video that belongs to that playlist.\n
Use the link in the share option of the playlist's page
'''

duration_interface = gr.Interface(
    fn=playlist_duration_calculator,
    inputs=[
        gr.Textbox(label="Playlist Link"),
        gr.Radio(["Total Duration", "Average Duration"], label="What to calculate?")
    ],
    outputs=gr.Textbox(label="Result"),
    title=heading,
    description=description
)

second_heading = "YouTube Playlist Mismatch Calculator"
second_description = "Enter two YouTube playlist links to compare their contents and find the mismatch."

def playlist_mismatch_calculator(playlist_link_1, playlist_link_2, output_options):
    result = playlists_mismatch_func(playlist_link_1, playlist_link_2, output_options)
    playlist1name = result[2]
    playlist2name = result[3]
    text = 'Present in {}, not in {} :- \n{} \n \nPresent in {}, not in {} :-\n {}'.format(
        playlist1name, playlist2name, '\n'.join(result[0]),
        playlist2name, playlist1name, '\n'.join(result[1])
    )
    return f"Mismatch Result between the two playlists are as follows: -\n\n{text}"

mismatch_interface = gr.Interface(
    fn=playlist_mismatch_calculator,
    inputs=[
        gr.Textbox(label="Playlist Link 1"),
        gr.Textbox(label="Playlist Link 2"),
        gr.Radio(["id", "link", "name"], label="Output Options")
    ],
    outputs=gr.Textbox(label="Mismatch between two playlists"),
    title=second_heading,
    description=second_description
)

combined_interface = gr.TabbedInterface(
    [duration_interface, mismatch_interface],
    ['Playlist Total and Average Duration', 'Playlist Mismatch']
)

combined_interface.launch()
