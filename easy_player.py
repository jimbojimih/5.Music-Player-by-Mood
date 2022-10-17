import os
import json

from ytmusicapi import YTMusic
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize, Qt, QTimer, QThread
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
        QMenu,
        QMessageBox
)

basepath = os.path.dirname(os.path.abspath(__file__))
dllspath = os.path.join(basepath, 'dlls')
os.environ['PATH'] = dllspath + os.pathsep + os.environ['PATH']
import mpv


class PlayListCreator(QThread):
    '''Get the url of the audio to be played by the player.'''
    def __init__(self):
        QMainWindow.__init__(self)
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
                    if video_id is not None:
                        tracks_from_playlist.append(video_id)
                list_all_video_id.append(tracks_from_playlist)
            self.play_lists_json[mood] = list_all_video_id

    def run(self):
        self.create_mood_list_of_video_id_dict()
        with open('play_lists.json', 'w') as file:
            json.dump(self.play_lists_json, file) 


class PlaybackControl():
    def __init__(self):
        self.player = mpv.MPV(video=False, ytdl=True)
        self.player.pause = True

        #last_tracks_played = LastTracksPlayed()
        self.last_tracks = LastTracksPlayed.open()

        self.play_list_load()

    def play_list_load(self):
        with open('play_lists.json', 'r') as file:
            self.play_lists_json = json.load(file)       

    def play(self, checked):
        self.player.pause = not checked

    def set_volume(self, value):
        self.player.volume = value

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

    def update_last_tracks_played(self):
        self.last_tracks[self.mood] = [self.player.playlist_pos, self.numb_playlist]

    def turn_on_the_next_playlist(self):
        len_playlist_of_mood = len(self.play_lists_json[self.mood]) - 1
        if self.numb_playlist < len_playlist_of_mood:
            self.player.stop()
            self.player.playlist_clear()
            self.numb_playlist += 1
            playlist = self.play_lists_json[self.mood][self.numb_playlist]

            for video_id in playlist:
                link = "https://www.youtube.com/watch?v=" + video_id
                self.player.playlist_append(link)

            self.player.playlist_pos = 0
        else: pass

    def turn_on_the_previous_playlist(self):
        if self.numb_playlist > 0:
            self.player.stop()
            self.player.playlist_clear()
            self.numb_playlist -= 1
            playlist = self.play_lists_json[self.mood][self.numb_playlist]

            for video_id in playlist:
                link = "https://www.youtube.com/watch?v=" + video_id
                self.player.playlist_append(link)

            self.player.playlist_pos = 0
        else: pass

    def get_video_id(self):
        return self.player.filename

    def check_the_last_track(self):
        if self.player.playlist_pos == -1:
            self.turn_on_the_next_playlist()    

    def save_the_last_track(self):
        LastTracksPlayed.save(self.last_tracks)
    

class LastTracksPlayed():
    @staticmethod
    def save(last_tracks):
        with open('last_track.json', 'w') as file:
            json.dump(last_tracks, file)

    @staticmethod        
    def open():
        with open('last_track.json', 'r') as file:
            last_track = json.load(file)
        return last_track

    @staticmethod
    #don't WORK!!! надо чтобы он забрал ласт трек из памяти и обнулил тоже
    def reset():
        reset_last_track_played = {"Chill": [0, 0], "Commute": [0, 0], "Energy Boosters": [0, 0], "Feel Good": [0, 0], "Focus": [0, 0], "Party": [0, 0], "Romance": [0, 0], "Sleep": [0, 0], "Workout": [0, 0]}
        LastTracksPlayed.save(reset_last_track_played)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.playback_control = PlaybackControl()
        self.playback_control.set_mood('Chill')

        self.timer = QTimer()
        self.timer.timeout.connect(self.set_title)
        self.timer.timeout.connect(lambda: self.playback_control.update_last_tracks_played())
        self.timer.timeout.connect(lambda: self.playback_control.check_the_last_track())
        self.timer.start(500)
        
        self.play_list_creator = PlayListCreator()

        self.menu = QMenuBar()         
        self.file_menu = QMenu('File')
        self.menu.addMenu(self.file_menu)
        self.file_menu.addAction('Update playlist', self.update_play_list)
        self.file_menu.addAction('Reset the save of lasts tracks played', lambda: LastTracksPlayed.reset())

        self.menu.addAction('About Easy Player', self.show_about_app_window)              
        
        self.button = QPushButton("Play")
        self.button.setCheckable(True)   
        self.button.setFixedSize(85, 30) 
        self.button.clicked.connect(self.play)

        self.button_return = QPushButton("<--")
        self.button_return.setFixedSize(85, 30) 
        self.button_return.clicked.connect(lambda: self.playback_control.turn_on_the_previous_playlist())

        self.next_playlist = QPushButton("-->") 
        self.next_playlist.setFixedSize(85, 30) 
        self.next_playlist.clicked.connect(lambda: self.playback_control.turn_on_the_next_playlist())

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(100)
        self.slider.setFixedSize(85, 20)
        self.slider.valueChanged.connect(self.volume)

        self.choice = QComboBox()

        self.choice.setFixedSize(100, 30)
        self.choice.addItems(["Chill", "Commute", "Energy Boosters"])
        self.choice.addItems(["Feel Good", "Focus", "Party"])
        self.choice.addItems(["Romance", "Sleep", "Workout"])
        self.choice.currentTextChanged.connect(self.set_mood)

        self.title = QLabel()
        self.title.setOpenExternalLinks(True)
        
        layout1 = QHBoxLayout()  

        layout1.addWidget(self.button_return)
        layout1.addWidget(self.button)
        layout1.addWidget(self.next_playlist)
        
        layout2 = QHBoxLayout()

        layout2.addWidget(self.slider)        
        layout2.addWidget(self.choice)

        layout3 = QVBoxLayout()  

        layout3.setMenuBar(self.menu)
        layout3.addLayout(layout1)  
        layout3.addStretch(1) 
        layout3.addLayout(layout2) 
        layout3.addStretch(1)                            
        layout3.addWidget(self.title) 

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
        video_id = self.playback_control.get_video_id()

        if self.playback_control.get_video_id() is not None:
            url_text = 'https://www.youtube.com/' + video_id
            url = "<a href=\"{url_text}\"> <font color=black>Open on YouTube</a>".format(url_text=url_text)
            self.title.setText(url)
        else:
            self.title.setText('wait')

    def show_about_app_window(self):
        text_title = 'About Easy Player'
        text = ('A simple music player to listen to music in the background,' 
                  'depending on your mood. Work is allowed on the playlists of ' 
                  'YouTube Music. If the music is not suitable for you, you can ' 
                  'switch the playlist. To do this, press --> or <-- '
                  'When the program is restored again, playback will start from ' 
                  'the last played track. To update playlists, ' 
                  'click "Update Audio Sources" \n\n'
                  'Простой музыкальный плеер для фонового прослушивания ' 
                  'музыки, в зависимости от выбранного настроения. Работа '
                  'программы основана на плейлистах YouTube Music. Если ' 
                  'музыка не подходит для Вас, вы можете переключить плейлист. '
                  'Для этого нажмите --> или <--. При повторном '
                  'запуске программы, вопроизведение начнётся с последнего '
                  'воспоизведённого трека. Для обновления плейлистов '
                  'нажмите "Update audio sources"')
        QMessageBox.information(self, text_title, text)

    def update_play_list(self):  
        self.update_play_list = PlayListCreator()

        text_title_finish_message = 'Done'
        text_finish_message = 'Playlists have been updated. You can reset the saving of the last played tracks. Playback will start with the updated playlists.'
        self.update_play_list.finished.connect(lambda: QMessageBox.information(self, text_title_finish_message, text_finish_message))
        self.update_play_list.start()

        text_title_warning_message = 'Update'
        text_warning_message = 'Please wait about 10 minutes. You can continue to use the player. The update takes place in the background. When the update is completed, you will see a notification.' 
        QMessageBox.warning(self, text_title_warning_message, text_warning_message)
 
    def closeEvent(self, event):
        self.playback_control.save_the_last_track()
        event.accept()

if __name__ == '__main__':  


    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
