from PySide6 import QtWidgets, QtCore, QtGui
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.side_menu_widget import SideMenu
from src.client.music_session import MusicSession 
from src.client.main_page_widget import MainPageMenu
import io
import eyed3
import settings
import random



class CurrentMusicWidget(AnimatedPanel):
    unlike_state: bool = False
    music_frame: MainPageMenu.MusicFrame = None
    pixmap: QtGui.QPixmap = None
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(CurrentMusicWidget, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.music_session: MusicSession = self.parent.music_session

        self.info_layout = QtWidgets.QHBoxLayout()
        self.info_widget = QtWidgets.QWidget()

        self.parent_title = QtWidgets.QLabel()
        self.hide_button = SideMenu.SideButton(self, 'hide', QtCore.QSize(28, 28))

        self.music_info_widget = QtWidgets.QFrame()
        self.music_info_layout = QtWidgets.QVBoxLayout()

        self.image_label = QtWidgets.QLabel()
        self.title_label = QtWidgets.QLabel()
        self.info_label = QtWidgets.QLabel()
        self.music_session_audio_timer = CurrentMusicWidget.MusicSessionAudioTimer(self) 

        self.buttons_widget = QtWidgets.QFrame()
        self.buttons_layout = QtWidgets.QHBoxLayout()

        button_size = QtCore.QSize(24, 24)

        self.play_button = SideMenu.SideButton(self, 'play', QtCore.QSize(48, 48))
        self.next_button = SideMenu.SideButton(self, 'next', button_size)
        self.previous_button = SideMenu.SideButton(self, 'previous', button_size)
        self.like_button = SideMenu.SideButton(self, 'like', button_size)
        self.unlike_button = SideMenu.SideButton(self, 'unlike', button_size)

        self.tools_widget = QtWidgets.QFrame()
        self.tools_layout = QtWidgets.QHBoxLayout()

        tool_size = QtCore.QSize(20, 20)

        self.loop_button = SideMenu.SideButton(self, 'repeat', tool_size)
        self.refresh_button = SideMenu.SideButton(self, 'randomize', tool_size)
        self.timer_button = SideMenu.SideButton(self, 'timer', tool_size)
        self.text_button = SideMenu.SideButton(self, 'text', tool_size)
    
    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.info_layout.setContentsMargins(5, 5, 5, 5)

        self.setContentsMargins(-8, 30, -10, 25)

        self.tools_layout.setContentsMargins(5, 5, 5, 5)

        self.image_label.setScaledContents(True)

        self.setObjectName('CurrentMusicWidget')
        self.music_info_widget.setObjectName('MusicInfoWidget')
        self.tools_widget.setObjectName('ToolsWidget')
        self.buttons_widget.setObjectName('ButtonsWidget')
        self.hide_button.setObjectName('HideButton')

        self.info_layout.addWidget(self.hide_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.info_layout.addWidget(self.parent_title, 1, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.info_layout.addSpacerItem(QtWidgets.QSpacerItem(35, 0))

        self.info_widget.setLayout(self.info_layout)

        self.music_info_layout.addWidget(self.image_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.music_info_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 10))
        self.music_info_layout.addWidget(self.title_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.music_info_layout.addWidget(self.info_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignLeft)
        
        self.music_info_widget.setLayout(self.music_info_layout)

        self.buttons_layout.addWidget(self.unlike_button)
        self.buttons_layout.addWidget(self.previous_button)
        self.buttons_layout.addWidget(self.play_button)
        self.buttons_layout.addWidget(self.next_button)
        self.buttons_layout.addWidget(self.like_button)

        self.buttons_widget.setLayout(self.buttons_layout)

        self.tools_layout.addWidget(self.loop_button)
        self.tools_layout.addWidget(self.refresh_button)
        self.tools_layout.addWidget(self.timer_button)
        self.tools_layout.addWidget(self.text_button)

        self.tools_widget.setLayout(self.tools_layout)

        self.main_v_layout.addWidget(self.info_widget, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_v_layout.addWidget(self.music_info_widget, 1, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 20))
        self.main_v_layout.addWidget(self.music_session_audio_timer, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.buttons_widget, 2, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_layout.addWidget(self.tools_widget, 1, QtCore.Qt.AlignmentFlag.AlignBottom)

        set_style_sheet_for_widget(self, 'current_music_widget.qss')

        self.music_session.playbackStateChanged.connect(self.on_state_changed)

        self.unlike_button.clicked.connect(self.unlike_button_clicked)
        self.previous_button.clicked.connect(self.previous_button_clicked)
        self.play_button.clicked.connect(self.play_button_clicked)
        self.next_button.clicked.connect(self.next_button_clicked)
        self.like_button.clicked.connect(self.like_button_clicked)

        self.loop_button.clicked.connect(self.loop_button_clicked)
        self.refresh_button.clicked.connect(self.refresh_button_clicked)
        self.text_button.clicked.connect(self.text_button_clicked)
        self.timer_button.clicked.connect(self.timer_button_clicked)
        self.hide_button.clicked.connect(self.hide_button_clicked)
    
    def on_state_changed(self, state) -> None:
        if state == MusicSession.PlaybackState.StoppedState and self.unlike_state:
            self.next_button_clicked()
            self.play_button_clicked()
            self.unlike_state = True
    
    def set_music(self, music_frame: MainPageMenu.MusicFrame) -> None:
        if music_frame:
            self.music_frame = music_frame
            music = music_frame.music
            self.title_label.setText(music.tag.title)
            self.info_label.setText(f'{music.tag.artist} • {music.tag.album}')
            if music.tag.images:
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(io.BytesIO(music.tag.images[0].image_data).getvalue())
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
                self.image_label.setFixedSize(155, 155)
            else:
                pixmap = QtGui.QPixmap(f'{settings.IMG_DIR}/default_track.png')
                self.pixmap = pixmap
                self.image_label.setPixmap(pixmap)
                self.image_label.setFixedSize(125, 125)

            self.play_button.pressed = False
            self.play_button.toggle_pressed()

            self.parent_title.setText(music_frame.parent.title_label.text())

            self.parent.music_info_widget.set_music(music_frame)
   
    def get_parent_widget(self) -> MainPageMenu:
        if not self.music_frame.parent.type:
            return self.parent.main_page_menu
        else:
            return self.parent.my_music_menu

    def loop_button_clicked(self) -> None:
        self.loop_button.toggle_pressed()
        if not self.loop_button.pressed:
            loop = MusicSession.Loops.Infinite
        else:
            loop = MusicSession.Loops.Once

        self.music_session.setLoops(loop)
        
    def refresh_button_clicked(self) -> None:
        self.refresh_button.toggle_pressed()

    def text_button_clicked(self) -> None:
        pass # TODO Вряд ли реализую. Подумаю еще

    def timer_button_clicked(self) -> None:
        pass # TODO

    def unlike_button_clicked(self) -> None:
        pass

    def previous_button_clicked(self) -> None:
        widget = self.get_parent_widget()

        if int(self.music_frame.objectName().split("-")[1]) - 1 < 1:
            id = widget.scroll_layout.count()
        else:
            id = int(self.music_frame.objectName().split("-")[1]) - 1 

        new_object_name = f'MusicFrame-{id}'

        self.music_frame.toggle_pressed()
        self.set_music(widget.findChild(MainPageMenu.MusicFrame, new_object_name))

        self.music_frame.set_audio(self)
        
    def play_button_clicked(self) -> None:
        self.music_frame.switch_function(self)

    def next_button_clicked(self) -> None:
        widget = self.get_parent_widget()

        if self.refresh_button.pressed:
            if int(self.music_frame.objectName().split("-")[1]) + 1 > widget.scroll_layout.count():
                id = 1 
            else:
                id = int(self.music_frame.objectName().split("-")[1]) + 1
        else:
            id = random.randint(1, self.music_frame.parent.scroll_layout.count())

        new_object_name = f'MusicFrame-{id}'
        
        self.music_frame.toggle_pressed()
        self.set_music(widget.findChild(MainPageMenu.MusicFrame, new_object_name))

        self.music_frame.set_audio(self)

    def like_button_clicked(self) -> None:
        self.parent.music_info_widget.like_button_clicked()
        if self.like_button.pressed:
            self.unlike_state = False
            self.hide_button.click()

    def hide_button_clicked(self) -> None:
        self.parent.widget_switch_animation(widget=self)

    class MusicSessionAudioTimer(QtWidgets.QFrame):
        def __init__(self, parent: QtWidgets.QWidget | None = ..., f: QtCore.Qt.WindowType = ...) -> None:
            super(CurrentMusicWidget.MusicSessionAudioTimer, self).__init__(parent)
            self.parent = parent
            self.__init_ui()
            self.__setting_ui()

        def __init_ui(self) -> None:
            self.main_h_layout = QtWidgets.QHBoxLayout()

            self.current_time_label = QtWidgets.QLabel('0:00')
            self.total_time_label = QtWidgets.QLabel('0:00')

            self.slider = CurrentMusicWidget.MusicSessionAudioTimer.Slider(self)

            self.calculate_timer = QtCore.QTimer(self)
            self.update_timer = QtCore.QTimer(self)
        
        def __setting_ui(self) -> None:
            self.setLayout(self.main_h_layout)

            self.setObjectName('MusicSessionAudioTimer')

            set_style_sheet_for_widget(self, 'music_session_audio_timer.qss')

            self.main_h_layout.addWidget(self.current_time_label)
            self.main_h_layout.addWidget(self.slider)
            self.main_h_layout.addWidget(self.total_time_label)

            self.calculate_timer.timeout.connect(self.calculate_time)
            self.update_timer.timeout.connect(self.update_time)

        def get_new_time_code(self) -> int:
            return (int(self.total_time.split(':')[0]) * 60 + int(self.total_time.split(':')[1])) / 100 * self.slider.value()
        
        def set_new_audio_code(self) -> None:
            self.parent.music_session.setPosition(int(self.get_new_time_code()) * 1000)

        def get_current_time(self) -> str:
            return f'{int(self.parent.music_session.position() / 1000 // 60)}:{int(self.parent.music_session.position() / 1000 % 60):02d}'
        
        def get_total_time(self) -> str:
            return f'{int(self.parent.music_session.duration() / 1000 // 60)}:{int(self.parent.music_session.duration() / 1000 % 60):02d}'

        def calculate_time(self) -> None:
            self.total_time = self.get_total_time()
            self.current_time = self.get_current_time()

        def update_time(self) -> None:
            self.total_time_label.setText(self.total_time)
            self.current_time_label.setText(self.current_time)
            if not self.slider.mouse_pressed:
                self.slider.setValue((self.parent.music_session.position() / 1000) / (self.parent.music_session.duration() / 1000) * 100)

        class Slider(QtWidgets.QSlider):
            current_time_slide: float = 0
            mouse_pressed: bool = False
            def __init__(self, parent) -> None:
                super(CurrentMusicWidget.MusicSessionAudioTimer.Slider, self).__init__(parent)
                self.parent = parent
                self.__setting_ui()

            def __setting_ui(self) -> None:
                self.setObjectName('Slider')

                self.setFixedWidth(self.width() + 140)

                set_style_sheet_for_widget(self, 'slider.qss')

                self.setValue(self.current_time_slide)
                self.setMinimum(0)
                self.setMaximum(100)
                self.setOrientation(QtCore.Qt.Orientation.Horizontal)
            
            def get_new_value(self, event) -> None:
                return self.minimum() + \
                        (event.x() / self.width()) * \
                        (self.maximum() - self.minimum())

            def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
                event.ignore()

            def mousePressEvent(self, event: QtGui.QMouseEvent):
                self.mouse_pressed = True

                new_value = self.get_new_value(event)

                self.setValue(new_value)

            def mouseMoveEvent(self, event: QtGui.QMouseEvent):
                if self.mouse_pressed:
                    new_value = self.get_new_value(event)

                    self.setValue(new_value)
            
            def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
                self.mouse_pressed = False
                self.parent.set_new_audio_code()


