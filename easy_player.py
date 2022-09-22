from ytmusicapi import YTMusic
from moviepy.editor import AudioFileClip
import os
import pafy

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, 'dlls')
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']
import mpv

mood_dict = {}
ytmusic = YTMusic()
ytmusic.setup
dict_ = ytmusic.get_mood_categories()
'''
for a in dict_['Moods & moments']:
    mood_dict[a['title']] = a['params']
#print(mood_dict)
'''

#print(ytmusic.get_mood_playlists(mood_dict['Chill'])[0])

#print(ytmusic.get_playlist('RDCLAK5uy_lFLL3kvPVwDnLJYBQuRmtP3-1_w63yUSk')['tracks'])

video_url = "https://www.youtube.com/watch?v=" + 'e4PBKgLlaHk'
video = pafy.new(video_url)
audio = video.getbestaudio()
audio_url = audio.url


#clip = AudioFileClip(audio_url)
#clip.preview(fps=44100)


player = mpv.MPV(ytdl=True)
player.play(audio_url)
player.wait_for_playback()
