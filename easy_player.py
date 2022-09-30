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
    QHBoxLayout,
    QWidget,
    QComboBox,
    QSlider,
    QLabel,
    QGridLayout
)

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, 'dlls')
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']

import mpv

dict_mood_and_parametrs = {}
ytmusic = YTMusic()
ytmusic.setup 
'''
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

for mood, param in dict_mood_and_parametrs.items():
    list_video_id = []
    for p in param:
        tracks_from_playlist = []
        tracks_from_playlist_raw = ytmusic.get_playlist(p)['tracks']
        for video_id in tracks_from_playlist_raw:
            tracks_from_playlist.append(video_id['videoId'])
        list_video_id.append(tracks_from_playlist)
    dict_mood_and_parametrs[mood] = list_video_id

with open('hight_score.json', 'w') as hs:
            json.dump(dict_mood_and_parametrs, hs) 

'''
with open('hight_score.json', 'r') as hs:
            hss = json.load(hs)
video_url = "https://www.youtube.com/watch?v=" + hss['Chill'][0][0]
video = pafy.new(video_url)
audio = video.getbestaudio()
audio_url = audio.url
print(video.title)



player = mpv.MPV(ytdl=True) #ytdl=True
player.playlist_append(audio_url)
#self.mpv_player.playlist_clear()
player.pause = True
player.playlist_pos = 0


class MainWindow(QWidget):
    def __init__(self, player, video):
        super().__init__()
        self.player = player 
        self.video = video
        #self.setStyleSheet("background-color: black;")

        self.button_return = QPushButton("<--")
        self.button_return.setFixedSize(85, 30) 
        #self.button_return.setFont((QFont('Arial', 8)))
        #self.button_return.clicked.connect(self.play)

        self.button = QPushButton("Play")
        self.button.setCheckable(True)   
        self.button.setFixedSize(85, 30) 
        self.button.clicked.connect(self.play)

        self.skeep = QPushButton("-->") 
        self.skeep.setFixedSize(85, 30) 
        #self.skeep.clicked.connect(self.play)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(100)
        self.slider.setFixedSize(85, 20)
        self.slider.valueChanged.connect(self.volume)

        self.choice = QComboBox()
        self.choice.setFixedSize(85, 30)
        self.choice.addItems(["Chill", "Power", "Three"])

        title = self.video.title
        self.name = QLabel(title)
        
        layout1 = QHBoxLayout()  #layout = QVBoxLayout()

        layout1.addWidget(self.button_return)
        layout1.addWidget(self.button)
        layout1.addWidget(self.skeep)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(self.slider)        
        layout2.addWidget(self.choice)

        layout3 = QVBoxLayout()  #layout = QVBoxLayout()
        layout3.addLayout(layout1)  
        layout3.addStretch(1) 
        layout3.addLayout(layout2) 
        layout3.addStretch(1)    
                        
        layout3.addWidget(self.name) 

        self.setLayout(layout3)
        self.setWindowTitle("Easy Player")
        self.setFixedWidth(300)
        self.setFixedHeight(130)
        self.show()
    def play(self, checked):
        self.player.pause = not checked
        if self.button.text() == "Play":
            self.button.setText('Pause')
        else: self.button.setText("Play")

    def volume(self, value):
        player.volume = value

app = QApplication([])

window = MainWindow(player, video)
window.show()

app.exec()
