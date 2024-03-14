from PySide6 import QtWidgets, QtCore, QtGui
from src.client.main_page_widget import MainPageMenu
from src.client.side_menu_widget import SideMenu
from src.client.tools.style_setter import set_style_sheet_for_widget
import eyed3


class MusicInfo(MainPageMenu.MusicFrame):
    def __init__(self, parent: QtWidgets.QWidget, music: eyed3.AudioFile) -> None:
        super().__init__(parent, music)
        self.__init_ui()
        self.__setting_ui()
        self.show()

    def __init_ui(self) -> None:
        self.play_button = SideMenu.SideButton(self, 'play.png', QtCore.QSize(22, 22))
        self.like_button = SideMenu.SideButton(self, 'like.png', QtCore.QSize(24, 24))

    def __setting_ui(self) -> None:
        self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.main_h_layout.setContentsMargins(5, 0, 5, 0)
        self.play_button.setContentsMargins(0, 5, 0, 5)
        self.like_button.setContentsMargins(0, 5, 0, 5)
        set_style_sheet_for_widget(self, 'music_info.qss')
        self.main_h_layout.insertWidget(0, self.like_button)
        self.main_h_layout.insertItem(0, QtWidgets.QSpacerItem(30, 0, QtWidgets.QSizePolicy.Policy.Preferred))
        self.main_h_layout.insertItem(self.main_h_layout.count(), QtWidgets.QSpacerItem(self.parent.size().width(), 0, QtWidgets.QSizePolicy.Policy.Preferred))
        self.main_h_layout.addWidget(self.play_button)