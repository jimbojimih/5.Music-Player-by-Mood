# 5.Music-Player-by-Mood
A simple music player with a GUI (PyQy6) to listen to music, depending on the selected mood. The program is based on YouTube Music playlists.

- The working principle is as follows:
>1) The PlayListCreator class creates a json file consisting of the video_id of the tracks, based on which links to YouTube Music are generated.
>2) The PlaybackControl class controls the playback of tracks. Switching between playlists happens automatically.
>3) The MainWindow class creates a graphical interface.
>4) The LastTracksPlayed class loads and saves the last played tracks.
>5) The video_id of the tracks is stored in play_lists.json as follows:
**{Mood_1: [[Video_id1 , Video_id2…], [Video_id1 , Video_id2…],…**
where [Video_id1 , Video_id2…] is a single YouTube Music playlist.
>6) The last listened tracks are stored in last_track.json in the following form:
**{ Mood_1: [0, 1],…**
>where 0 is the track number in the playlist, 1 is the playlist number for the selected mood.

- There is an option to update playlists ("update_play_list" button). The update takes place in a separate thread that does not affect the operation of the player.

- To install the necessary modules, enter the command (preferably in a virtual environment) - pip install python-mpv ytmusicapi PyQt6 youtube-dl pyinstaller

- Download the library required for MPV to work here https://sourceforge.net/projects/mpv-player-windows/files/libmpv/ The library must be placed in the "dlls" folder in the project folder.
yt-dlp.exe required for ytmusicapi to work, download here https://github.com/yt-dlp/yt-dlp

- The code is completely ready to build with pyinstaller.
To do this, enter the command
**pyinstaller --onefile --icon=icon.ico --collect-all "ytmusicapi" --add-binary "yt-dlp.exe;." --noconsole --add-data "dlls/mpv-2.dll;." --add-data "icon.png;." easy_player.py**
Then place two files, play_lists.json and last_track.json, in the same directory as the .exe executable.
---
Простой музыкальный плеер с графическим интерфейсом(PyQy6) для прослушивания музыки, в зависимости от выбранного настроения. Работа программы основана на плейлистах YouTube Music. 

- Принцип работы следующий: 
>1)	Класс PlayListCreator создаёт json-файл, состоящий из video_id треков, на основе которых генерируются ссылки на YouTube Music.
>2)	Класс PlaybackControl управляет воспроизведением треков. Переключение между плейлистами происходит автоматически.
>3)	Класс MainWindow создаёт графический интерфейс.
>4)	Класс LastTracksPlayed загружает и сохраняет последние проигранные треки.
>5) Video_id треков сохраняется в play_lists.json в следующем виде:  
**{Mood_1: [[Video_id1 , Video_id2…], [Video_id1 , Video_id2…],…**  
где [Video_id1 , Video_id2…] является отдельным плейлистом YouTube Music.
>6) Последние прослушанные треки сохраняется в last_track.json в следующем виде:  
**{ Mood_1: [0, 1],…**  
>где 0 – номер трека в плейлисте, 1 – номер плейлиста для выбранного настроения.

- Существует возможность обновления плейлистов («update_play_list» button). Обновление происходит в отельном потоке, не влияющем на работу плеера.

- Для установки необходимых модулей введите команду (желательно в виртуально среде) – pip install python-mpv ytmusicapi PyQt6 youtube-dl pyinstaller

- Библиотеку, необходимую для работы MPV, скачать тут https://sourceforge.net/projects/mpv-player-windows/files/libmpv/ Библиотеку необходимо поместить в папку "dlls" в папке проекта.  
yt-dlp.exe, необходимый для работы ytmusicapi, скачать тут https://github.com/yt-dlp/yt-dlp  

- Код полностью готов к сборке с помощью pyinstaller. 
Для этого введите команду   
**pyinstaller --onefile --icon=icon.ico --collect-all "ytmusicapi" --add-binary "yt-dlp.exe;." --noconsole --add-data "dlls/mpv-2.dll;." --add-data "icon.png;." easy_player.py**   
Затем поместите в один каталог вместе с исполняемым файлом .exe два файла: play_lists.json и last_track.json. 
