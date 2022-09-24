import os
import time
from tkinter import *

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
def pause():
    player.pause = True
def resume():
    player.pause = False
def play():   
    player.playlist_pos = 0

              
root = Tk()
root.geometry('600x300')    
Label(root, text = 'g', font='lucidia 30 bold').pack()
Button(text='play', command=play).place(x=200, y=100)
Button(text='pause', command=pause).place(x=250, y=100)
Button(text='resume', command=resume).place(x=150, y=100)
root.mainloop()


'''
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("Clicked!")


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
'''
