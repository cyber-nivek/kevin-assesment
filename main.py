from googleapiclient.discovery import build
from yt_dlp import YoutubeDL
import whisper
import tkinter as tk
from tkinter import simpledialog
import googleapiclient.errors as gerror
import os

"""" Loads whisper model locally if exists, downloads it if not.
Processes given audio file, transcribe its dialog, stores it in a text file in a preset folder """


def audioTranscription(path, filename, debug_mode):
    model = whisper.load_model("base")
    try:
        audio = whisper.load_audio(path + "/" + filename + ".mp3")
    except:
        print("model could not load audio file")
        return
    try:
        result = model.transcribe(audio)
    except:
        print("Error while transcribing")
        return
    with open(path + filename + ".txt", 'w') as f:
        f.write(result['text'])
    if debug_mode == "True":
        print(result)



""""# For a given channel name, locates and returns its ID"""


def getChannelId(youtube, channel_name):
    request = youtube.search().list(part='snippet', q=channel_name, type='channel')
    try:
        expected_channel = request.execute()
    except:
        print("Could not find Channel ID. Exiting")
        exit()
    return expected_channel['items'][0]['id']['channelId']


"""For a given channel ID, returns the playlist "uploads", ie the uploaded content. Also shorts."""


def getUploadPlaylist(youtube, channel_id):
    request = youtube.channels().list(part='contentDetails', id=channel_id)
    try:
        channel_contents = request.execute()
    except:
        print("Cannot get upload playlist (uploaded videos). Exiting")
        exit()
    return channel_contents['items'][0]['contentDetails']['relatedPlaylists']['uploads']


"""Returns all video id from a playlist. It isn't actually all of them tho, just the num defined in maxResults"""

def getVideosFromPlaylist(youtube, playlist_id):
    request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=2)
    try:
        playlist_contents = request.execute()
    except:
        print("Video fetch from playlist failed. Exiting")
        exit()
    video_list = []
    for item in playlist_contents['items']:
        if item['kind'] == "youtube#playlistItem":
            video_list.append(item['contentDetails']['videoId'])
    return video_list


"""Gets audio from a yt video and stores it locally for later transcription"""


def extractAudio(video_url):
    audio_downloader = YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '/temp/%(title)s.mp3'})
    try:
        info_dict = audio_downloader.extract_info(video_url, download=True)
    except:
        print("Audio download failed")
    video_title = info_dict['title']
    return video_title


"""Lil neat program that seeks a given youtube video or channel, and extracts the videos transcription in a txt file"""

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    google_ID = simpledialog.askstring("Please input your Google API", "Google API ID")
    if not google_ID:
        print("Google_ID was not introduced")
        exit()
    channel_name = simpledialog.askstring("Input video link OR Channel name", "Channel Name OR Video URL")
    if not channel_name:
        print("Channel name (or video url) was not provided")
        exit()
    debug_mode = simpledialog.askstring("Debug Mode", "Enable Debug Mode (True or False")
    if not debug_mode:
        debug_mode = False
    try:
        youtube = build('youtube', 'v3', developerKey=google_ID)
    except:
        print("Uh-oh! Conection Failed for some reason. Exiting")
        exit()

    url_template = "https://www.youtube.com/watch?v="
    # We'll know if it's no actually a channel at this point
    if url_template in channel_name:
        file = extractAudio(channel_name)
        if file:
            audioTranscription('temp/', file, debug_mode)

    # Seems it was not, so transcripting several of the (latest) channel videos
    else:
        channel_id = getChannelId(youtube, channel_name)
        playlist_id = getUploadPlaylist(youtube, channel_id)
        video_list = getVideosFromPlaylist(youtube, playlist_id)
        for video_url in video_list:
            file = extractAudio(url_template + video_url)
            if file:
                audioTranscription('temp/', file, debug_mode)
