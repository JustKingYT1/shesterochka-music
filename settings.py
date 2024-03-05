import os, sys


# Global settings

DEBUG = True
MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.executable), os.pardir)) if not DEBUG \
            else os.path.abspath(os.path.join(os.path.dirname(sys.executable), os.pardir, os.pardir))


# Database settings

DB_PATH = f'{MAIN_DIR}/resources/shesterochkaPlayer.db'

# Client settings

CONFIG_PATH = f'{MAIN_DIR}/resources/config.json'
IMG_DIR = f'{MAIN_DIR}/resources/img'
MUSIC_DIR = f'{MAIN_DIR}/resources/musics'