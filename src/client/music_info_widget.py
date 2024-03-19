from PySide6 import QtWidgets, QtCore, QtGui
from src.client.main_page_widget import MainPageMenu
from src.client.side_menu_widget import SideMenu
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.database_models import User, UserPlaylists, Music
import eyed3


class MusicInfo(MainPageMenu.MusicFrame):
    def __init__(self, parent: QtWidgets.QWidget, music: eyed3.AudioFile) -> None:
        super(MusicInfo, self).__init__(parent, music)
        self.__init_ui()
        self.__setting_ui()
        self.show()

    def __init_ui(self) -> None:
        self.play_button = SideMenu.SideButton(self, 'play', QtCore.QSize(22, 22))
        self.like_button = SideMenu.SideButton(self, 'like', QtCore.QSize(24, 24))

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

        self.play_button.setEnabled(False)
        self.like_button.setEnabled(False)

        self.play_button.clicked.connect(self.play_button_clicked)
        self.like_button.clicked.connect(self.like_button_clicked)

    def add_music_to_profile(self) -> None:
        if self.like_button.pressed:
            UserPlaylists.create(user_id=self.parent.session.user.id, music_id=self.music.tag.id)
        else:
            UserPlaylists.get((UserPlaylists.user_id==self.parent.session.user.id) & (UserPlaylists.music_id == self.music.tag.id)).delete_instance()
        
        self.like_button.toggle_pressed()
        self.parent.main_page_menu.reload_tracks(self.parent.main_page_menu.type)
        self.parent.my_music_menu.reload_tracks(self.parent.my_music_menu.type)
    
            # GET OR NONE UserPlaylists((user_id == user_id, music_id == music_id) но 
             # music_id у нас нет по умолчанию, поэтому 
             # Для его получения ищем в Music(title == title, artist == artist)) если есть, то 
             # Искусственно изменяю состояние кнопки
             # Если нет, то ничего не делаю, и чтобы 
             # При нажатии кнопки в обратную сторону
             # Удалял из избранного трек идиотка тупая

    def like_button_clicked(self) -> None:
        self.add_music_to_profile()

    def play_button_clicked(self) -> None:
        self.switch_function()

    def set_music(self, music: eyed3.AudioFile) -> None:
        self.play_button.pressed = False
        self.play_button.toggle_pressed()
        self.change_music(music)
    
    def change_music(self, music: eyed3.AudioFile) -> None:
        self.title_label.setText(music.tag.title)
        self.info_label.setText(f'{music.tag.artist} • {music.tag.album}')
        self.music = music
