from PySide6 import QtCore, QtGui, QtMultimedia
from src.client.main_page_widget import MainPageMenu
import eyed3


class MusicSession(QtMultimedia.QMediaPlayer):
    audio_output: QtMultimedia.QAudioOutput = None
    current_music: eyed3.AudioFile = None
    widget = None
    def __init__(self, parent) -> None:
        super(MusicSession, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.audio_output = QtMultimedia.QAudioOutput()
        self.stop_timer = QtCore.QTimer(self)

    def __setting_ui(self) -> None:
        self.setAudioOutput(self.audio_output)
        self.stop_timer.timeout.connect(self.stop_timer_slot)

    def start_stop_timer(self, seconds: int) -> None:
        self.stop_timer.start(seconds * 1000)
    
    def stop_timer_slot(self) -> None:
        self.stop()
        self.stop_timer.stop()
        self.parent.current_music_widget.timer_button.toggle_pressed()
        self.parent.music_info_widget.music_widget.change_play_buttons_state()

    def setSource(self, source: QtCore.QUrl | str, widget: MainPageMenu.MusicFrame) -> None:
        super().setSource(source)
        self.current_music = widget.music
        self.widget = widget
