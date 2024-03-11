import os
import settings
import eyed3


def get_music_in_music_dir(sort: bool = False):
    files = [eyed3.load(os.path.join(settings.MUSIC_DIR, file)) \
             for file in os.listdir(settings.MUSIC_DIR) \
                if file.endswith('.mp3')]
    
    for file in files:
        if not file.tag:
            file.initTag()
            file.tag.title = 'Unknown'
            file.tag.artist = 'Unknown'
            file.tag.album = 'Unknown'
            file.tag.save()

    return files if not sort else sorted(files, key=lambda x: x.tag.title)