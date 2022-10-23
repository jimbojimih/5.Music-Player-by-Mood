# 5.Music-Player-by-Mood
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

- «!»Код полностью готов к сборке с помощью pyinstaller. 
Для этого введите команду – pyinstaller --onefile --icon=icon.ico --collect-all "ytmusicapi" --add-binary "yt-dlp.exe;." --noconsole --add-data "dlls/mpv-2.dll;." --add-data "icon.png;." easy_player.py

- Библиотеку, необходимую для работы MPV, скачать тут https://sourceforge.net/projects/mpv-player-windows/files/libmpv/
yt-dlp.exe, необходимый для работы ytmusicapi, скачать тут https://github.com/yt-dlp/yt-dlp
Затем поместите в один каталог вместе с .exe два файла: play_lists.json и last_track.json. 
