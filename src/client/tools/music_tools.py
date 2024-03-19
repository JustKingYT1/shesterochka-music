import os
import settings
import eyed3
from src.database_models import UserPlaylists, Music


def get_music_in_music_dir(sort: bool = False, my_music_flag: bool=False, user_id: int=None):
    if not my_music_flag:
        files = [eyed3.load(f'{settings.MUSIC_DIR}/{file}') \
             for file in os.listdir(settings.MUSIC_DIR) \
                if file.endswith('.mp3')] 
    else:
        files = []
        records = UserPlaylists.select().where(UserPlaylists.user_id == user_id)
        for record in records:
            files.append(eyed3.load(Music.get(Music.id == record.music_id).path))

    for file in files:
        if not file.tag:
            file.initTag()

        if file.tag.title != 'Unknown' and file.tag.artist != 'Unknown':
            file.tag.id = Music.get((Music.title==file.tag.title) & (Music.artist==file.tag.artist))

        file.tag.album = 'Unknown' if not file.tag.album else file.tag.album
        file.tag.title = 'Unknown' if not file.tag.title else file.tag.title
        file.tag.artist = 'Unknown' if not file.tag.artist else file.tag.artist
        
        file.tag.save()

    return files if not sort else sorted(files, key=lambda x: x.tag.title)