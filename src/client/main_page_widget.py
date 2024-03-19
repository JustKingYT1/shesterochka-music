from PySide6 import QtWidgets, QtCore, QtGui
from eyed3 import AudioFile
from src.client.tools.music_tools import get_music_in_music_dir
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.animated_panel_widget import AnimatedPanel
from io import BytesIO
import settings
import time
import enum


class TypesMenu(enum.Enum):
    MyMusic: bool = True
    MainMusic: bool = False


class MainPageMenu(AnimatedPanel):
    def __init__(self, parent: QtWidgets.QWidget, type: TypesMenu) -> None:
        super(MainPageMenu, self).__init__(parent)
        self.parent = parent
        self.type = type
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.music_list: list = []

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.setObjectName('MainPageMenu')

        set_style_sheet_for_widget(self, 'main_page_menu.qss')
        if self.parent.session.user.id == -1 and self.type:
            self.set_notification('Авторизуйтесь для использования приложения')
            return

        self.main_v_layout.addWidget(self.scroll_area)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setMaximumWidth(6)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setObjectName('ScrollArea')
        self.scroll_area.verticalScrollBar().setObjectName('ScrollBar')

        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_widget.setObjectName('ScrollWidget')

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.load_music(self.type)

    def load_track(self, music: AudioFile) -> None:
        # Music.create(title=music.tag.title, artist=music.tag.artist, path=music.path)
        new_music_frame: MainPageMenu.MusicFrame = MainPageMenu.MusicFrame(self.parent, music)
        self.scroll_layout.addWidget(new_music_frame)
        new_music_frame.size_expand()
        self.music_list.append(new_music_frame)
    
    def clear_musics(self) -> None:
        for music in self.music_list:
            music.close()

        self.music_list.clear()
    
    def set_notification(self, text: str) -> None:
        title = QtWidgets.QLabel()
        title.setText(text)
        title.setObjectName('TitleLabel')
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addItem(QtWidgets.QSpacerItem(0, self.width() // 2, QtWidgets.QSizePolicy.Policy.Expanding, \
                                                            QtWidgets.QSizePolicy.Policy.Expanding))
        self.main_v_layout.addWidget(title)
        self.main_v_layout.addItem(QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Policy.Fixed))
        button = QtWidgets.QPushButton()
        button.setText('Настройки')
        self.main_v_layout.addWidget(button)
        button.clicked.connect(self.parent.side_menu.settings_button.click)
        button.setObjectName('ToSettingsButton')
        button.setMinimumSize(50, 30)
        self.main_v_layout.addItem(QtWidgets.QSpacerItem(0, self.width() // 2 + 40, QtWidgets.QSizePolicy.Policy.Expanding,\
                                                         QtWidgets.QSizePolicy.Policy.Expanding))
        
    def reload_widget(self, only_clear: bool=False) -> None:
        layout = self.main_v_layout
        self.music_list.clear()
        while layout.count():
            item = layout.itemAt(0)
            widget = item.widget()
            spacer = item.spacerItem()

            if widget:
                widget.deleteLater()
                layout.removeWidget(widget)
                del widget
            elif spacer:
                layout.removeItem(spacer) 
                del spacer

        if not only_clear:
            self.__init_ui()
            self.__setting_ui()
    
    def reload_tracks(self, my_music_flag: bool=False) -> None:
        self.clear_musics()
        self.load_music(my_music_flag)
    
    def load_music(self, my_music_flag: bool=False) -> None:
        files: list = get_music_in_music_dir(True, my_music_flag, self.parent.session.user.id if self.type else None)

        print(self.parent.session.user.id )

        for file in files:
            if 'empty.mp3' in file.path:
                continue
            self.load_track(file)

    def size_expand(self) -> None:
        self.resize(self.parent.width() - 20, self.parent.height() - 55)
        for music in self.music_list:
            music.size_expand()
        
    class MusicFrame(QtWidgets.QFrame):
        music: AudioFile
        toggle: bool = False
        def __init__(self, parent: QtWidgets.QWidget, music: AudioFile) -> None:
            super(MainPageMenu.MusicFrame, self).__init__(parent)
            self.parent = parent
            self.music = music
            self.main_win = self.parent

            self.__init_ui()
            self.__setting_ui()

        def __init_ui(self) -> None:
            self.main_h_layout = QtWidgets.QHBoxLayout()
            self.info_v_layout = QtWidgets.QVBoxLayout()
            self.title_label = QtWidgets.QLabel(self.music.tag.title)
            self.info_label = QtWidgets.QLabel(f'{self.music.tag.artist} • {self.music.tag.album}')
            self.image_label = QtWidgets.QLabel()

        def __setting_ui(self) -> None:
            self.setLayout(self.main_h_layout)
            self.setObjectName('MusicFrame')
            self.main_h_layout.setContentsMargins(0, 0, 0, 0)
            self.main_h_layout.insertItem(0, QtWidgets.QSpacerItem(4, 0))
            self.main_h_layout.addWidget(self.image_label)
            self.image_label.setScaledContents(True)
            self.image_label.setFixedSize(30, 30)
            self.main_h_layout.addSpacerItem(QtWidgets.QSpacerItem(5, 0, QtWidgets.QSizePolicy.Policy.Fixed))
            self.main_h_layout.addLayout(self.info_v_layout)
            self.info_v_layout.addWidget(self.title_label)
            self.info_v_layout.addWidget(self.info_label)

            self.info_label.setObjectName('InfoLabel')

            self.image_label.setObjectName('ImageLabel')

            if self.music.tag.images:
                pixmap: QtGui.QPixmap = QtGui.QPixmap()
                pixmap.loadFromData(BytesIO(self.music.tag.images[0].image_data).getvalue())
                self.image_label.setPixmap(pixmap)
            
            else:
                pixmap: QtGui.QPixmap = QtGui.QPixmap(f"{settings.IMG_DIR}/default_track.png")
                self.image_label.setPixmap(pixmap)

        def toggle_pressed(self) -> None:
            if not self.toggle:
                self.setStyleSheet('''  
                        QFrame#MusicFrame{
                            background-color: rgba(95, 95, 95, 128);
                        }
                                   
                        QFrame#MusicFrame::hover{
                            background-color: rgba(55, 55, 55, 128);
                        }
                    ''')
            else:
                self.setStyleSheet('''  
                        QFrame#MusicFrame{
                            background-color: rgba(70, 70, 70, 128);
                        }
                                   
                        QFrame#MusicFrame::hover{
                            background-color: rgba(85, 85, 85, 128);
                        }
                    ''')
                
            self.toggle = not self.toggle

        def play(self) -> None:
            self.main_win.music_session.play()
            self.main_win.music_info_widget.play_button.toggle_pressed()

        def pause(self) -> None:
            self.main_win.music_session.pause()
            self.main_win.music_info_widget.play_button.toggle_pressed()
        
        def stop(self) -> None:
            self.main_win.music_session.stop()

        def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
            self.switch_function()

        def switch_function(self) -> None:
            self.set_audio()
            if self.main_win.music_session.isPlaying():
                self.pause()
            else:
                self.play()
            
        
        def set_audio(self) -> None:
            if not self.main_win.music_session.current_music or self.main_win.music_session.current_music.path != self.music.path:
                self.stop()
                time.sleep(0.01)
                self.main_win.change_current_music_widget_style()
                self.main_win.music_session.setSource(QtCore.QUrl().fromLocalFile(self.music.path), self)
                self.main_win.music_info_widget.set_music(self.music)
                self.main_win.change_state_like_button()
                self.toggle_pressed()

        def size_expand(self) -> None:
            self.setFixedWidth(self.parent.width() - 42)
