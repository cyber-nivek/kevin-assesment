from googleapiclient.discovery import build
from yt_dlp import YoutubeDL
import whisper
import googleapiclient.errors
import os


def audioTranscription(path, filename):
    model = whisper.load_model("base")
    audio = whisper.load_audio(path+"/"+filename+".mp3")
    # audio = whisper.pad_or_trim(audio)
    result = model.transcribe(audio)
    with open(path+filename+".txt", 'w') as f:
        f.write(result['text'])

def getChannelId(youtube, channel_name):
    request = youtube.search().list(part='snippet', q=channel_name, type='channel')
    expected_channel = request.execute()
    return expected_channel['items'][0]['id']['channelId']

def getUploadPlaylist(youtube, channel_id):
    request = youtube.channels().list(part='contentDetails', id=channel_id)
    channel_contents = request.execute()
    return channel_contents['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def getVideosFromPlaylist(youtube, playlist_id):
    request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id, maxResults=3)
    playlist_contents = request.execute()
    video_list = []
    for item in playlist_contents['items']:
        if item['kind'] == "youtube#playlistItem":
            video_list.append(item['contentDetails']['videoId'])
    return video_list


def extractAudio(video_url):
    audio_downloader = YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': '/temp/%(title)s.mp3'})
    info_dict = audio_downloader.extract_info(video_url, download=True)
    video_title = info_dict['title']
    return video_title


if __name__ == "__main__":
    channel_name = "ThePrimeTime"
    youtube = build('youtube', 'v3', developerKey='AIzaSyBWL9EvVx0aeb4TbBKm22J9dBTk1IsD4Lw')
    channel_id = getChannelId(youtube, channel_name)
    playlist_id = getUploadPlaylist(youtube, channel_id)
    url_template = "https://www.youtube.com/watch?v="
    video_list = getVideosFromPlaylist(youtube, playlist_id)
    for video_url in video_list:
        file = extractAudio(url_template + video_url)
        audioTranscription('temp/', file)
