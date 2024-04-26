from PySide6 import QtWidgets, QtCore, QtGui
from eyed3 import AudioFile
from src.client.tools.music_tools import get_music_per_id, fill_database
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.tools.pixmap_tools import get_pixmap
from src.client.animated_panel_widget import AnimatedPanel
from src.database_models import Music, UserPlaylists, NotLikeMusic
from io import BytesIO
import settings
import time
import enum
import threading
  

class TypesMenu(enum.Enum):
    MyMusic: bool = 1
    MainMusic: bool = 0
    DeletedMusic: bool = 2

class MainPageMenu(AnimatedPanel):
    stop_flag: bool = False
    add_music_signal: QtCore.Signal = QtCore.Signal(AudioFile,)
    remove_widget_signal: QtCore.Signal = QtCore.Signal(QtWidgets.QLayout, QtCore.QObject,)
    def __init__(self, parent: QtWidgets.QWidget, type: TypesMenu) -> None:
        super(MainPageMenu, self).__init__(parent)
        self.parent = parent
        self.type = type.value
        self.__init_ui()
        self.__setting_ui()
        self.add_music_signal.connect(self.load_track)
        self.remove_widget_signal.connect(self.remove_widget)
    
    def __init_ui(self) -> None:
        self.title_label = QtWidgets.QLabel()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.search_widget = MainPageMenu.SearchWidget(self)

        self.list_musics: list[MainPageMenu.MusicFrame] = []
        self.update_thread: threading.Thread = None
        self.num = 1

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.setObjectName('MainPageMenu')

        self.setContentsMargins(-6, 30, -10, 20)

        set_style_sheet_for_widget(self, 'main_page_menu.qss')
        if self.parent.session.user.id == -1 and self.type == TypesMenu.MyMusic.value:
            self.set_notification('Авторизуйтесь для использования своей музыки')
            self.search_widget.hide()
            return
        
        if self.type == TypesMenu.MainMusic.value:
            title = '<h2>Главная</h2>'
        elif self.type == TypesMenu.MyMusic.value:
            title = '<h2>Моя музыка</h2>'
        elif self.type == TypesMenu.DeletedMusic.value:
            title = '<h2>Удаленная музыка</h2>'

        self.title_label.setText(title)

        self.title_label.setObjectName('TitleLabel')

        self.main_v_layout.addWidget(self.title_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.title_label.setFixedWidth(self.parent.height() - 187)

        self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 5))

        self.main_v_layout.addWidget(self.scroll_area)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.verticalScrollBar().setMaximumWidth(6)
        self.scroll_area.setContentsMargins(0,0,0,0)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setObjectName('ScrollArea')
        self.scroll_area.verticalScrollBar().setObjectName('ScrollBar')

        self.scroll_layout.setContentsMargins(0,0,0,0)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_widget.setObjectName('ScrollWidget')

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.main_v_layout.addWidget(self.search_widget)

    def set_title(self, title: str) -> None:
        self.title_label.setText(f'<h1>{title}</h1>')
    
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
        
    def clear_musics(self) -> None:            
        for music in self.list_musics:
            music.close()
        
    def reload_widget(self, layout: QtWidgets.QVBoxLayout, only_clear: bool=False) -> None: # TODO
        while layout.count(): # Заменить способ удаления или хранения музыки
            item = layout.itemAt(0)
            widget = item.widget()
            spacer = item.spacerItem()

            if widget:
                self.remove_widget_signal.emit(layout, widget)
            elif spacer: 
                self.remove_widget_signal.emit(layout, spacer)

        if not only_clear:
            self.__init_ui()
            self.__setting_ui()

    @QtCore.Slot(AudioFile,)
    def load_track(self, music: AudioFile) -> None:
        new_music_frame: MainPageMenu.MusicFrame = MainPageMenu.MusicFrame(self, music)
        new_music_frame.size_expand()
        new_music_frame.setObjectName(f'MusicFrame-{self.num}')
        new_music_frame.setStyleSheet(f'''
            
            QFrame#MusicFrame-{self.num}{{
                background-color: rgba(70, 70, 70, 86);
                border-radius: 10px;
            }}

            QFrame#MusicFrame-{self.num}::hover{{
                background-color: rgba(95, 95, 95, 86);
            }}

            QFrame#MusicFrame-{self.num}>QLabel{{
                color: white;
            }}

            QFrame#MusicFrame-{self.num}s>QLabel#InfoLabel{{
                color: rgb(150, 150, 150);
            }}
        ''')
        self.scroll_layout.addWidget(new_music_frame)
        self.num += 1
        self.list_musics.append(new_music_frame)

    @QtCore.Slot(QtWidgets.QLayout, QtCore.QObject,)
    def remove_widget(self, layout: QtWidgets.QLayout, item: QtCore.QObject) -> None:
        layout.removeWidget(item) if isinstance(item, QtWidgets.QWidget) else layout.removeItem(item)
        item.deleteLater() if isinstance(item, QtWidgets.QWidget) else None
        item.close() if isinstance(item, MainPageMenu.MusicFrame) else None
        
    def update_music(self, reload: bool = False) -> None:
        if self.update_thread:
            self.update_thread.join()
        self.update_thread = threading.Thread(target=self.load_music, args=[reload,])
        self.update_thread.start()
    
    def get_list_musics_id(self) -> list[int]:
        if self.type == TypesMenu.MainMusic.value:
            return range(1, Music.select().count() + 1)
        elif self.type == TypesMenu.MyMusic.value:
            return [elem.music_id for elem in UserPlaylists.select().where(UserPlaylists.user_id == self.parent.session.user.id)]
        elif self.type == TypesMenu.DeletedMusic.value:
            return [elem.music_id for elem in NotLikeMusic.select().where(NotLikeMusic.user_id == self.parent.session.user.id)]

    def load_music(self, reload: bool = False) -> None:
        list_search_musics: list | bool = self.search_widget.search_musics()
        list_unliked_music: list = NotLikeMusic.select().where(NotLikeMusic.user_id == self.parent.session.user.id)
        flag = False if list_search_musics else True
        if reload and self.scroll_layout.count() > 0:
            self.clear_musics()
        if Music.select().count() == 0:
            fill_database()
        
        for id in self.get_list_musics_id():
            if self.stop_flag:
                exit()

            music: AudioFile = get_music_per_id(id)

            if list_search_musics and len(list_search_musics) > 0:
                for title in list_search_musics:
                    if title == music.tag.title:
                        flag = True
                        break

            if list_unliked_music and len(list_unliked_music) > 0 and self.type != TypesMenu.DeletedMusic.value:
                for elem in list_unliked_music:
                    if elem.music_id.id == music.tag.id:
                        flag = False
                        break

            time.sleep(0.01)
            self.add_music_signal.emit(music) if flag else None
            flag = False if list_search_musics else True

    def size_expand(self) -> None:
        self.resize(self.parent.width() - 13.5, self.parent.height() - 72.5)
    
    class SearchWidget(QtWidgets.QFrame):
        last_click_time = QtCore.QDateTime.currentDateTime()
        search_text: str = ''
        def __init__(self, parent: QtWidgets.QWidget) -> None:
            super().__init__(parent)
            self.parent = parent
            self.__init_ui()
            self.__setting_ui()

        def __init_ui(self) -> None:
            self.main_h_layout = QtWidgets.QHBoxLayout()
            self.search_button = QtWidgets.QPushButton()
            self.search_line_edit = QtWidgets.QLineEdit()

        def __setting_ui(self) -> None:
            self.setLayout(self.main_h_layout)

            self.setObjectName('SearchWidget')

            self.search_button.setIcon(get_pixmap('search.png'))
            self.search_button.setIconSize(QtCore.QSize(28, 28))

            self.main_h_layout.setContentsMargins(3, 3, 3, 3)
            self.main_h_layout.addWidget(self.search_button)
            self.main_h_layout.addWidget(self.search_line_edit)

            self.search_line_edit.textChanged.connect(self.set_search_text)

            self.search_button.clicked.connect(lambda: self.parent.update_music(True))

            self.size_expand()
        
        def size_expand(self) -> None:
            self.setFixedWidth(self.parent.parent.width() - 34)
            
            self.search_line_edit.setFixedHeight(26.5)

            self.search_button.setFixedSize(28, 28)
        
        def set_search_text(self) -> None:
            self.search_text = self.search_line_edit.text()
            if self.search_text == '':
                current_time = QtCore.QDateTime.currentDateTime()
                if current_time.secsTo(self.last_click_time) >= -1:
                    self.last_click_time = current_time
                    return
                self.search_button.click()
                self.last_click_time = current_time

        def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
            current_time = QtCore.QDateTime.currentDateTime()
            if current_time.secsTo(self.last_click_time) >= -1:
                self.last_click_time = current_time
                return
            if event.key() == QtCore.Qt.Key.Key_Return.numerator:
                self.search_button.click()
            self.last_click_time = current_time

        def search_musics(self) -> list | None:
            layout: QtWidgets.QLayout = self.parent.scroll_layout
            list_musics: list[MainPageMenu.MusicFrame] = []
            for i in range(0, layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()

                if widget:
                    if self.search_text.lower() in widget.title_label.text().lower() and self.search_text != '':
                        list_musics.append(widget.title_label.text())

            return None if not len(list_musics) > 0 and self.search_text == '' else list_musics
        
    class MusicFrame(QtWidgets.QFrame):
        music: AudioFile
        toggle: bool = False
        pixmap: QtGui.QPixmap
        def __init__(self, parent: QtWidgets.QWidget, music: AudioFile) -> None:
            super(MainPageMenu.MusicFrame, self).__init__(parent)
            self.parent = parent
            self.music = music
            self.main_win = self.parent.parent

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
                mask = QtGui.QBitmap(pixmap.size())
                mask.fill(QtCore.Qt.GlobalColor.color0)
                painter = QtGui.QPainter(mask)
                painter.setBrush(QtCore.Qt.GlobalColor.color1)
                path = QtGui.QPainterPath()
                radius = 120
                painter.drawRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
                painter.fillPath(path, QtCore.Qt.GlobalColor.color1)
                painter.end()
                pixmap.setMask(mask)
                self.pixmap = pixmap
                self.image_label.setPixmap(pixmap)
            
            else:
                pixmap: QtGui.QPixmap = QtGui.QPixmap(f"{settings.IMG_DIR}/default_track.png")
                self.pixmap = pixmap
                self.image_label.setPixmap(pixmap)

        def toggle_pressed(self) -> None:
            if not self.isAncestorOf(self):
                if not self.toggle:
                    self.setStyleSheet(f'''  
                            QFrame#MusicFrame-{self.objectName().split('-')[1]}{{
                                background-color: rgba(95, 95, 95, 86);
                                border-radius: 10px;

                            }}
                                    
                            QFrame#MusicFrame-{self.objectName().split('-')[1]}::hover{{
                                background-color: rgba(55, 55, 55, 86);
                                border-radius: 10px;
                            }}
                        ''')
                else:
                    self.setStyleSheet(f'''  
                            QFrame#MusicFrame-{self.objectName().split('-')[1]}{{
                                background-color: rgba(70, 70, 70, 86);
                                border-radius: 10px;
                            }}
                                    
                            QFrame#MusicFrame-{self.objectName().split('-')[1]}::hover{{
                                background-color: rgba(85, 85, 85, 86);
                                border-radius: 10px;
                            }}
                        ''')
                    
                self.toggle = not self.toggle

        def play(self) -> None:
            self.main_win.music_session.play()
            self.change_play_buttons_state()

        def change_play_buttons_state(self) -> None:
            self.main_win.music_info_widget.play_button.toggle_pressed()
            self.main_win.current_music_widget.play_button.toggle_pressed()

        def pause(self) -> None:
            self.main_win.music_session.pause()
            self.change_play_buttons_state()

        def stop(self) -> None:
            self.main_win.music_session.stop()

        def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
            self.switch_function(self)
            self.main_win.widget_switch_animation(widget=self.main_win.opened_widget)

        def switch_function(self, widget: QtWidgets.QWidget) -> None:
            self.set_audio(widget)
            if self.main_win.music_session.isPlaying():
                self.pause()
            else:
                self.play()
        
        def set_audio(self, widget: QtWidgets.QWidget) -> None:
            if not self.main_win.music_session.current_music or self.main_win.music_session.current_music.path != self.music.path:
                self.stop()
                time.sleep(0.01)
                self.main_win.change_current_music_widget_style()
                self.main_win.music_session.setSource(QtCore.QUrl().fromLocalFile(self.music.path), self)
                self.main_win.music_info_widget.set_music(self) if not widget == self.main_win.music_info_widget.music_frame else None
                self.main_win.current_music_widget.set_music(self) if not widget == self.main_win.current_music_widget.music_frame else None
                self.main_win.change_state_like_button(self.main_win.music_info_widget)
                self.main_win.change_state_like_button(self.main_win.current_music_widget)
                self.main_win.current_music_widget.music_session_audio_timer.calculate_timer.start(400)
                self.main_win.current_music_widget.music_session_audio_timer.update_timer.start(550)
        
                self.toggle_pressed()

        def size_expand(self) -> None:
            self.setFixedWidth(self.main_win.width() - 37)
