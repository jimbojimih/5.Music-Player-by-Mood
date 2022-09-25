import os
import time

from ytmusicapi import YTMusic
import pafy
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, 'dlls')
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']

import mpv


ytmusic = YTMusic()
ytmusic.setup
get_raw_dict = ytmusic.get_mood_categories()
dict_mood_and_parametrs = {}

for a in get_raw_dict['Moods & moments']:
    dict_mood_and_parametrs[a['title']] = a['params']


first_chill_playlist = ytmusic.get_mood_playlists(dict_mood_and_parametrs['Chill'])[0]

playlist_id = first_chill_playlist['playlistId']

track_list_from_playlist = ytmusic.get_playlist(playlist_id)['tracks']

video_id = track_list_from_playlist[0]['videoId']

video_url = "https://www.youtube.com/watch?v=" + video_id
video = pafy.new(video_url)
audio = video.getbestaudio()
audio_url = audio.url

player = mpv.MPV(ytdl=True) #ytdl=True
player.playlist_append(audio_url)
#print(player.volume)
#self.mpv_player.playlist_clear()
player.pause = True
player.playlist_pos = 0


class MainWindow(QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setWindowTitle("Easy Player")
        self.button = QPushButton("Play")
        self.button.setCheckable(True)
        self.button.clicked.connect(self.play)
        self.setCentralWidget(self.button)

    def play(self, checked):
        self.player.pause = not checked
        if self.button.text() == "Play":
            self.button.setText('Pause')
        else: self.button.setText("Play")
app = QApplication([])

window = MainWindow(player)
window.show()

app.exec()

