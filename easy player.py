from ytmusicapi import YTMusic
from pytube import YouTube
import pygame
from moviepy.editor import AudioFileClip
import time
from threading import Thread
'''
mood_dict = {}
ytmusic = YTMusic()
ytmusic.setup
dict_ = ytmusic.get_mood_categories()

for a in dict_['Moods & moments']:
    mood_dict[a['title']] = a['params']
#print(mood_dict)
sleep(1)
'''
#print(ytmusic.get_mood_playlists(mood_dict['Chill'])[0])

#print(ytmusic.get_playlist('RDCLAK5uy_lFLL3kvPVwDnLJYBQuRmtP3-1_w63yUSk')['tracks'])
start_time=time.time()
video_url = "https://www.youtube.com/watch?v=" + 'e4PBKgLlaHk'






'''
with io.BytesIO() as file_buffer:
    yt.streams.get_audio_only().stream_to_buffer(file_buffer)
'''
def g(video_url, b):
    yt = YouTube(video_url)
    yt.streams.get_audio_only().download(filename=b)
    clip = AudioFileClip(b)
    clip.preview(fps=44100)

q = ['https://music.youtube.com/watch?v=4NRXx6U8ABQ&list=RDCLAK5uy_mQZP3pxJWK85P-5yltO4YgsYC-Xvk9_Bc', video_url]
r = ['1.mp4', '2.mp4']
for video_url, b in zip(q, r):
    thread = Thread(target=g, args=(video_url, b))
    thread.start()
print(start_time - time.time())
'''
yt2 = YouTube('https://music.youtube.com/watch?v=4NRXx6U8ABQ&list=RDCLAK5uy_mQZP3pxJWK85P-5yltO4YgsYC-Xvk9_Bc')
yt2.streams.get_audio_only().download(filename='2.mp4')
clip2 = AudioFileClip('1.mp4')
clip.preview(fps=44100)
'''


'''

url = ''
req = requests.get(url)
res = io.BytesIO(req.content)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(res)
pygame.mixer.music.play()

'''
