import os
import settings
import eyed3


def get_music_in_music_dir(sort: bool = False):
    files = [eyed3.load(f'{settings.MUSIC_DIR}/{file}') \
             for file in os.listdir(settings.MUSIC_DIR) \
                if file.endswith('.mp3')]

    for file in files:
        if not file.tag:
            file.initTag()

        file.tag.album = 'Unknown' if not file.tag.album else file.tag.album
        file.tag.title = 'Unknown' if not file.tag.title else file.tag.title
        file.tag.artist = 'Unknown' if not file.tag.artist else file.tag.artist
        
        file.tag.save()

    return files if not sort else sorted(files, key=lambda x: x.tag.title)