import os
# import sys

# sys.path.append('C:/shesterochka-music')

import settings
import eyed3
from src.database_models import Music


def fill_database(sort: bool = False):
    files = [(eyed3.load(f'{settings.MUSIC_DIR}/{file}'), file) \
            for file in os.listdir(settings.MUSIC_DIR) \
            if file.endswith('.mp3') and file != 'empty.mp3'] 

    for file, title in files:
        if not file.tag:
            file.initTag()

            file.tag.album = 'Неизвестен' if not file.tag.album else file.tag.album
            file.tag.title = title.split('.')[0] if not file.tag.title else file.tag.title
            file.tag.artist = 'Неизвестен' if not file.tag.artist else file.tag.artist
            
            file.tag.save()
        
        Music.create(title=file.tag.title, path=file.path, artist=file.tag.artist)


def get_music_per_id(id: int) -> eyed3.AudioFile:
    model = Music.get(Music.id == id)
    file = eyed3.load(model.path)

    if not file.tag:
        file.initTag()

        file.tag.album = 'Неизвестен' if not file.tag.album else file.tag.album
        file.tag.title = model.title if not file.tag.title else file.tag.title
        file.tag.artist = 'Неизвестен' if not file.tag.artist else file.tag.artist
        file.tag.save()

    file.tag.id = Music.get((Music.title==file.tag.title) & (Music.artist==file.tag.artist)).id

    return file


# Music.get(Music.id == 119).delete_instance()