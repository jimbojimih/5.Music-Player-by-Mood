import os
import time

import json
from ytmusicapi import YTMusic
import pafy
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (    
    QDial,
    QPushButton,
    QRadioButton,
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QWidget
)

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, 'dlls')
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']

import mpv

json_file = {}
dict_mood_and_parametrs = {}
ytmusic = YTMusic()
ytmusic.setup 

mood_dict = ytmusic.get_mood_categories()
for a in mood_dict['Moods & moments']:
    dict_mood_and_parametrs[a['title']] = a['params']

for mood, param in dict_mood_and_parametrs.items():
    dict_mood_and_parametrs[mood] = ytmusic.get_mood_playlists(param)

for mood, param in dict_mood_and_parametrs.items(): 
    list_playlist_id = []   
    for p in param:
        list_playlist_id.append(p['playlistId'])
    dict_mood_and_parametrs[mood] = list_playlist_id
#________________________________________________________________
for mood, param in dict_mood_and_parametrs.items():
    list_video_id = []
    for p in param:
        dic = dict()
        tracks_from_playlist = []
        tracks_from_playlist_raw = ytmusic.get_playlist(p)['tracks']
        for video_id in tracks_from_playlist_raw:
            tracks_from_playlist.append(video_id['videoId'])
        dic[p] = tracks_from_playlist
        list_video_id.append(dic)
    #print(list_video_id)
    dict_mood_and_parametrs[mood] = list_video_id

with open('hight_score.json', 'w') as hs:
            json.dump(dict_mood_and_parametrs, hs) 
#print(dict_mood_and_parametrs)
#first_chill_playlist = ytmusic.get_mood_playlists(dict_mood_and_parametrs['Chill'])[0]


'''
playlist_id = first_chill_playlist['playlistId']

track_list_from_playlist = ytmusic.get_playlist(playlist_id)['tracks']

video_id = track_list_from_playlist[0]['videoId']

video_url = "https://www.youtube.com/watch?v=" + video_id
video = pafy.new(video_url)
audio = video.getbestaudio()
audio_url = audio.url
'''
'''
player = mpv.MPV(ytdl=True) #ytdl=True
player.playlist_append(audio_url)
#self.mpv_player.playlist_clear()
player.pause = True
player.playlist_pos = 0


class MainWindow(QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.setWindowTitle("Easy Player")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        layout = QVBoxLayout()

        widget = QWidget()
        widget.setLayout(layout)

        self.button = QPushButton("Play")
        self.button.setCheckable(True)
        self.button.setGeometry(100, 100, 600, 400)        
        self.button.clicked.connect(self.play)

        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.setValue(100)
        self.dial.valueChanged.connect(self.volume)

        layout.addWidget(self.button)
        layout.addWidget(self.dial)
        

        self.setCentralWidget(widget)

    def play(self, checked):
        self.player.pause = not checked
        if self.button.text() == "Play":
            self.button.setText('Pause')
        else: self.button.setText("Play")

    def volume(self, value):
        player.volume = value

app = QApplication([])

window = MainWindow(player)
window.show()

app.exec()
'''