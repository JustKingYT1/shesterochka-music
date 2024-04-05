from PySide6 import QtCore, QtGui, QtMultimedia
from src.client.main_page_widget import MainPageMenu
import eyed3


class MusicSession(QtMultimedia.QMediaPlayer):
    audio_output: QtMultimedia.QAudioOutput = None
    current_music: eyed3.AudioFile = None
    widget = None
    def __init__(self, parent) -> None:
        super(MusicSession, self).__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.audio_output = QtMultimedia.QAudioOutput()

    def __setting_ui(self) -> None:
        self.setAudioOutput(self.audio_output)

        self.mediaStatusChanged.connect(self.on_media_status_changed)

    def on_media_status_changed(self, status) -> None:
        if status == QtMultimedia.QMediaPlayer.MediaStatus.EndOfMedia:
            print(1)

    def setSource(self, source: QtCore.QUrl | str, widget: MainPageMenu.MusicFrame) -> None:
        super().setSource(source)
        self.current_music = widget.music
        self.widget = widget
