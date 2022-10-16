import os
import json

from ytmusicapi import YTMusic
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtWidgets import (  
        QPushButton,
        QMainWindow,
        QApplication,
        QVBoxLayout,
        QHBoxLayout,
        QWidget,
        QComboBox,
        QSlider,
        QLabel,
        QMenuBar,
        QMenu
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
        self.ytmusic.setup

    def create_mood_param_dict(self):
        '''Get a dictionary with mood parameters.'''        
        mood_dict = self.ytmusic.get_mood_categories()
        for mood in mood_dict['Moods & moments']:
            self.play_lists_json[mood['title']] = mood['params']  

    def create_mood_playlists_id_dict(self):
        '''Get a dictionary with mood playlists.'''
        self.create_mood_param_dict()
        for mood, params in self.play_lists_json.items():
            self.play_lists_json[mood] = self.ytmusic.get_mood_playlists(params)        

    def create_clean_mood_playlists_id_dict(self):
        '''Get a dictionary with clean mood playlists. '''
        self.create_mood_playlists_id_dict()
        for mood, params in self.play_lists_json.items(): 
            list_playlist_id = []   
            for param in params:
                    list_playlist_id.append(param['playlistId'])
            self.play_lists_json[mood] = list_playlist_id

    def create_mood_list_of_video_id_dict(self):
        '''Get a dictionary with clean mood playlists.'''
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
        with open('play_lists.json', 'w') as file:
            json.dump(self.play_lists_json, file) 


class PlaybackControl():
    def __init__(self):
        self.player = mpv.MPV(video=False)
        self.player.pause = True

        self.last_tracks_played = LastTracksPlayed()
        self.last_tracks = self.last_tracks_played.open()

    def json_load(self):
        with open('play_lists.json', 'r') as file:
            self.play_lists_json = json.load(file)       

    def play(self, checked):
        self.player.pause = not checked

    def set_volume(self, value):
        self.player.volume = value

    def get_filename(self):
        return self.player.filename

    def set_mood(self, mood): 
        self.mood = mood

        self.player.stop()
        self.player.playlist_clear()
        
        pos_track, self.numb_playlist = self.last_tracks[self.mood]
        playlist = self.play_lists_json[self.mood][self.numb_playlist]       

        for video_id in playlist:
            link = "https://www.youtube.com/watch?v=" + video_id
            self.player.playlist_append(link)

        self.player.playlist_pos = pos_track   
        #print(self.player.playlist_count)
        #print(self.player.playlist_pos)

    def update_last_tracks_played(self):
        self.last_tracks[self.mood] = [self.player.playlist_pos, self.numb_playlist]

    def save_the_last_track(self):
        self.last_tracks_played.save(self.last_tracks)
    

class LastTracksPlayed():
    def save(self, last_tracks):
        with open('last_track.json', 'w') as file:
            json.dump(last_tracks, file)

    def open(self):
        with open('last_track.json', 'r') as file:
            last_track = json.load(file)
        return last_track


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.playback_control = PlaybackControl()
        self.playback_control.json_load()
        self.playback_control.set_mood('Chill')

        self.timer = QTimer()
        self.timer.timeout.connect(self.set_title)
        self.timer.timeout.connect(lambda: self.playback_control.update_last_tracks_played())
        self.timer.start(500)

        self.about_window = AboutWindow()

        self.menu = QMenuBar()         
        self.file_menu = QMenu('File')
        self.menu.addMenu(self.file_menu)
        self.file_menu.addAction('Update audio sources', lambda: print('a'))
        self.file_menu.addAction('Reset the save', lambda: print('b'))

        self.about_menu = QMenu('About Easy Player') 
        self.menu.addMenu(self.about_menu)                
        self.about_menu.aboutToShow.connect(lambda: self.about_window.show())
        
        self.button = QPushButton("Play")
        #self.button.setStyleSheet('border-style: solid; border-width: 1px; border-color: black; border-radius: 15px')
        self.button.setCheckable(True)   
        self.button.setFixedSize(85, 30) 
        self.button.clicked.connect(self.play)

        self.button_return = QPushButton("<--")
        #self.button_return.setStyleSheet('border-style: solid; border-width: 1px; border-color: black; border-radius: 15px')
        self.button_return.setFixedSize(85, 30) 
        #self.button_return.clicked.connect(self.play)

        self.skeep = QPushButton("-->") 
        self.skeep.radius = 170
        #self.skeep.setStyleSheet('border-style: solid; border-width: 1px; border-color: black; border-radius: 15px')

        self.skeep.setFixedSize(85, 30) 
        #self.skeep.clicked.connect(self.play)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(100)
        self.slider.setFixedSize(85, 20)
        self.slider.valueChanged.connect(self.volume)

        self.choice = QComboBox()
        #self.choice.setStyleSheet('border-style: solid; border-width: 1px; border-color: black;')

        self.choice.setFixedSize(100, 30)
        self.choice.addItems(["Chill", "Commute", "Energy Boosters"])
        self.choice.addItems(["Feel Good", "Focus", "Party"])
        self.choice.addItems(["Romance", "Sleep", "Workout"])
        self.choice.currentTextChanged.connect(self.set_mood)

        self.name = QLabel()
        self.name.setOpenExternalLinks(True)
        
        layout1 = QHBoxLayout()  

        layout1.addWidget(self.button_return)
        layout1.addWidget(self.button)
        layout1.addWidget(self.skeep)
        
        layout2 = QHBoxLayout()

        layout2.addWidget(self.slider)        
        layout2.addWidget(self.choice)

        layout3 = QVBoxLayout()  

        layout3.setMenuBar(self.menu)
        layout3.addLayout(layout1)  
        layout3.addStretch(1) 
        layout3.addLayout(layout2) 
        layout3.addStretch(1)                            
        layout3.addWidget(self.name) 

        self.setLayout(layout3)
        self.setWindowTitle("Easy Player")
        self.setFixedWidth(300)
        self.setFixedHeight(130)
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

    def play(self, checked):
        self.playback_control.play(checked)
        if self.button.text() == "Play":
            self.button.setText('Pause')
        else: self.button.setText("Play")

    def volume(self, value):
        self.playback_control.set_volume(value)

    def set_mood(self, currentText):
        self.playback_control.set_mood(currentText)  

    def set_title(self):
        text = 'https://www.youtube.com/' + self.playback_control.get_filename()
        #url = "<a href=\"http://www.google.com\">'Open on YouTube'</a>"
        url = "<a href=\"{url}\"> <font color=black>Open on YouTube</a>".format(url=text)
        self.name.setText(url)
 
    def closeEvent(self, event):
        self.playback_control.save_the_last_track()
        event.accept()

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()        
        text_en = ('A simple music player to listen to music in the background,' 
                  'depending on your mood. Work is allowed on the playlists of' 
                  '\nYouTube Music programs. To switch playlist, press --> or <--.'
                  'When the program is restored again, playback will start from\n' 
                  'the last played track. To update playlists update,' 
                  ' click "Update Audio Sources"')
        text_ru = ('Простой музыкальный плеер для фонового прослушивания ' 
                  'музыки, в зависимости от выбранного настроения.\nРабота '
                  'программы основана на плейлистах YouTube Music. Для '
                  'переключения плейлиста нажмите --> или <--.\nПри повторном '
                  'запуске программы, вопроизведение начнётся с последнего '
                  'воспоизведённого трека.\nДля обновления обновления плейлистов '
                  'нажмите "Update audio sources"')
        self.label_en = QLabel(text_en)
        self.label_en.setFont(QFont('Arial', 11))
        self.label_ru = QLabel(text_ru)
        self.label_ru.setFont(QFont('Arial', 11))
        layout.addWidget(self.label_en)
        layout.addWidget(self.label_ru)
        self.setLayout(layout)
        self.setWindowIcon(QIcon('icon.png'))

if __name__ == '__main__':  


    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
