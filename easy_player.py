import os
import json

from ytmusicapi import YTMusic
import pafy
from PyQt6.QtCore import Qt
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
    QGridLayout,
)

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, 'dlls')
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']
import mpv


class PlayListCreator():
    '''Get the url of the audio to be played by the player.'''
    def __init__(self):
        self.play_lists_json = {}
        self.ytmusic = YTMusic()         

    def create_mood_param_dict(self):
        '''Get a dictionary with mood parameters. 

        Example: "{'Chill': 'ggMPOg1uX0prdzllTXdBWmdM'..."

        '''
        self.ytmusic.setup
        mood_dict = self.ytmusic.get_mood_categories()
        for mood in mood_dict['Moods & moments']:
            self.play_lists_json[mood['title']] = mood['params']

    def create_mood_playlists_id_dict(self):
        '''Get a dictionary with mood playlists.

        Example: "{'Chill': [{'title': 'Russian Lounge', 

                'playlistId': 'RDCLAK5uy_lFLL3kvPVwDnLJYBQuRmtP3-1_w63yUS'..."

        '''
        self.create_mood_param_dict()
        for mood, params in self.play_lists_json.items():
            self.play_lists_json[mood] = self.ytmusic.get_mood_playlists(params)        

    def create_clean_mood_playlists_id_dict(self):
        '''Get a dictionary with clean mood playlists.

        Example: "{'Chill': ['RDCLAK5uy_lFLL3kvPVwDnLJYBQuRmtP3-1_w63yUS',..."

        '''
        self.create_mood_playlists_id_dict()
        for mood, params in self.play_lists_json.items(): 
            list_playlist_id = []   
            for param in params:
                    list_playlist_id.append(param['playlistId'])
            self.play_lists_json[mood] = list_playlist_id

    def create_mood_list_of_video_id_dict(self):
        '''Get a dictionary with clean mood playlists.

        Example: "{"Chill": [["e4PBKgLlaHk", "WaryKVQ1rhk"], 
                            [""0ZSWUAOYlSA", "dRHBDPpex1Y"]...

        '''
        self.create_clean_mood_playlists_id_dict()
        for mood, params in self.play_lists_json.items():
            list_all_video_id = []
            for param in params:
                tracks_from_playlist = []
                tracks_from_playlist_raw = self.ytmusic.get_playlist(param)['tracks']
                for track in tracks_from_playlist_raw:
                    video_id = track['videoId']
                    tracks_from_playlist.append(video_id)
                list_all_video_id.append(tracks_from_playlist)
            self.play_lists_json[mood] = list_all_video_id

    def create_json(self):
        self.create_mood_list_of_video_id_dict()
        with open('play_lists.json', 'w') as hs:
            json.dump(self.play_lists_json, hs) 


class AudioLinkCreator():
    def open_play_lists_json(self):
        with open('play_lists.json', 'r') as file:
            self.videos_id = json.load(file)

    def open_video_id(self, mood, playlist, track):
        self.video_url = ("https://www.youtube.com/watch?v=" + 
                        str(self.videos_id[mood][playlist][track]))
        try: 
            self.video = pafy.new(self.video_url)
        except: 
            self.audio_url = None   
        else:
            self.audio = self.video.getbestaudio()
            self.audio_url = self.audio.url
            self.audio_title = self.video.title
        
    def get_url(self):
        return self.audio_url

    def get_title(self):
        return self.video.title


class PlaybackControl():
    def __init__(self):
        self.audio_link = AudioLinkCreator()
        self.audio_link.open_play_lists_json()
        self.audio_link.open_video_id('Chill', 0, 0)
        link = self.audio_link.get_url()

        self.player = mpv.MPV(ytdl=True) #ytdl=True
        self.player.playlist_append(link)
        #self.mpv_player.playlist_clear()
        self.player.pause = True
        self.player.playlist_pos = 0 

    def play(self, checked):
        self.player.pause = not checked

    def set_volume(self, value):
        self.player.volume = value

    def get_title(self):
        return self.audio_link.get_title()



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.playback_control = PlaybackControl()
        #self.setStyleSheet("background-color: yellow;")

        self.button_return = QPushButton("<--")
        self.button_return.setFixedSize(85, 30) 
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
        self.choice.setFixedSize(90, 30)
        self.choice.addItems(["Chill", "Commute", "Energy Boosters"])
        self.choice.addItems(["Feel Good", "Focus", "Party"])
        self.choice.addItems(["Romance", "Sleep", "Workout"])

        title = self.playback_control.get_title()
        self.name = QLabel(title)
        
        layout1 = QHBoxLayout()  

        layout1.addWidget(self.button_return)
        layout1.addWidget(self.button)
        layout1.addWidget(self.skeep)
        
        layout2 = QHBoxLayout()
        layout2.addWidget(self.slider)        
        layout2.addWidget(self.choice)

        layout3 = QVBoxLayout()  
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
        self.playback_control.play(checked)
        if self.button.text() == "Play":
            self.button.setText('Pause')
        else: self.button.setText("Play")

    def volume(self, value):
        self.playback_control.set_volume(value)

#if __name__ == '__main__':  


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
