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

playlist_link_input = gr.inputs.Textbox(label="Playlist Link")
calculation_type_input = gr.inputs.Radio(["Total Duration", "Average Duration"], label="What to calculate?")
outputs = gr.outputs.Textbox(label="Result")

heading = "YouTube Playlist Duration Calculator"
description = "Enter a YouTube playlist link and choose the calculation type to calculate its total duration or average duration."


interface1 = gr.Interface(
    fn=playlist_duration_calculator,
    inputs=[playlist_link_input, calculation_type_input],
    outputs=outputs,
    title=heading,
    description=description,
    examples=[
        ["https://www.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS", "Total Duration"],
        ["https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p", "Average Duration"],
    ],
    theme="compact",
)

second_heading = "YouTube Playlist Mismatch Calculator"
second_description = "Enter two YouTube playlist links (without quotation marks) to compare their contents and find the mismatch."
mismatch_outputs = gr.outputs.Textbox(label="Mismatch between two playlists")

def playlist_mismatch_calculator(playlist_link_1, playlist_link_2, output_options):
    result = playlists_mismatch_func(playlist_link_1, playlist_link_2, output_options)
    playlist1name = result[2]
    playlist2name = result[3]
    text = 'Present in {}, not in {} :- \n{} \n \nPresent in {}, not in {} :-\n {}'.format(result[2],result[3], '\n'.join(result[0]), result[3], result[2], '\n'.join(result[1]))
    return f"Mismatch Result between the two playlists are as follows: -\n\n {text}"

playlist_link_1_input = gr.inputs.Textbox(label="Playlist Link 1")
playlist_link_2_input = gr.inputs.Textbox(label="Playlist Link 2")
output_options = gr.inputs.Radio(["id", "link", "name"], label="Output Options")

interface2 = gr.Interface(
    fn=playlist_mismatch_calculator,
    inputs=[playlist_link_1_input, playlist_link_2_input, output_options],
    outputs=mismatch_outputs,
    title=second_heading,
    description=second_description,
    # examples=[
    #     ["https://www.youtube.com/playlist?list=PL-osiE80TeTsWmV9i9c58mdDCSskIFdDS", "https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p"],
    # ],
    theme="compact",
)


# interface1.launch()    
# interface2.launch()

combinedinterface = gr.TabbedInterface([interface1,interface2],['Playlist Total and Average Duration', 'Playlist Mismatch'])

combinedinterface.launch()