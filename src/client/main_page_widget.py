from PySide6 import QtWidgets, QtCore, QtGui
from eyed3 import AudioFile
from src.client.tools.music_tools import get_music_in_music_dir
from io import BytesIO
import settings


class MainPageMenu(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(MainPageMenu, self).__init__(parent)
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setMaximumWidth(6)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

    def load_music() -> None:
        pass # TODO

        
    class MusicFrame(QtWidgets.QFrame):
        def __init__(self, parent: QtWidgets.QWidget, track: AudioFile) -> None:
            super().__init__(parent)

            self.track = track

            self.__init_ui()
            self.__setting_ui()

        def __init_ui(self) -> None:
            self.main_h_layout = QtWidgets.QHBoxLayout()
            self.album_and_artist_h_layout = QtWidgets.QHBoxLayout()
            self.info_v_layout = QtWidgets.QVBoxLayout()
            self.title_label = QtWidgets.QLabel(self.track.tag.title)
            self.info_label = QtWidgets.QLabel(f'{self.track.tag.artist} • {self.track.tag.album}')
            self.image_label = QtWidgets.QLabel()

        def __setting_ui(self) -> None:
            self.setLayout(self.main_h_layout)
            self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            self.main_h_layout.setContentsMargins(0, 0, 0, 0)
            self.main_h_layout.addWidget(self.image_label)
            self.main_h_layout.addLayout(self.info_v_layout)
            self.info_v_layout.addWidget(self.title_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
            self.info_v_layout.addLayout(self.info_label)

            if self.track.tag.images:
                pixmap: QtGui.QPixmap = QtGui.QPixmap()
                pixmap.loadFromData(BytesIO(self.track.tag.images[0].image_data).getvalue())
                self.image_label.setPixmap(pixmap)
            
            else:
                pixmap: QtGui.QPixmap = QtGui.QPixmap(f"{settings.IMG_DIR}/default_track.png")
                self.image_label.setPixmap(pixmap)



