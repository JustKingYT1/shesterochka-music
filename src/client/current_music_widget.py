from PySide6 import QtWidgets, QtCore, QtGui
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.side_menu_widget import SideMenu


class CurrentMusicWidget(AnimatedPanel):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(CurrentMusicWidget, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.hide_button = SideMenu.SideButton(self, 'hide', QtCore.QSize(28, 28))

        self.music_info_widget = QtWidgets.QFrame()
        self.music_info_layout = QtWidgets.QVBoxLayout()

        self.image_label = QtWidgets.QLabel('Image')
        self.title_label = QtWidgets.QLabel('Title')
        self.info_label = QtWidgets.QLabel('Artist • Album')
        self.time_slider = QtWidgets.QLabel('Time slider') # TODO

        self.buttons_widget = QtWidgets.QFrame()
        self.buttons_layout = QtWidgets.QHBoxLayout()

        button_size = QtCore.QSize(24, 24)

        self.play_button = SideMenu.SideButton(self, 'play', QtCore.QSize(36, 36))
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

        self.setContentsMargins(-8, 30, -10, 25)

        self.tools_layout.setContentsMargins(5, 5, 5, 5)

        self.setObjectName('CurrentMusicWidget')
        self.music_info_widget.setObjectName('MusicInfoWidget')
        self.tools_widget.setObjectName('ToolsWidget')
        self.buttons_widget.setObjectName('ButtonsWidget')
        self.hide_button.setObjectName('HideButton')

        self.music_info_layout.addWidget(self.image_label)
        self.music_info_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 10))
        self.music_info_layout.addWidget(self.title_label)
        self.music_info_layout.addWidget(self.info_label)
        self.music_info_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 10))
        self.music_info_layout.addWidget(self.time_slider)
        
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

        self.main_v_layout.addWidget(self.hide_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.main_v_layout.addWidget(self.music_info_widget, 1, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_layout.addWidget(self.buttons_widget, 1, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_layout.addWidget(self.tools_widget, 1, QtCore.Qt.AlignmentFlag.AlignBottom)

        set_style_sheet_for_widget(self, 'current_music_widget.qss')

        self.loop_button.clicked.connect(self.loop_button_clicked)
        self.refresh_button.clicked.connect(self.refresh_button_clicked)
        self.text_button.clicked.connect(self.text_button_clicked)
        self.timer_button.clicked.connect(self.timer_button_clicked)
        self.hide_button.clicked.connect(self.hide_button_clicked)
    
    def set_music(self, music) -> None:
        pass # TODO

    def loop_button_clicked(self) -> None:
        self.loop_button.toggle_pressed()

    def refresh_button_clicked(self) -> None:
        self.refresh_button.toggle_pressed()

    def text_button_clicked(self) -> None:
        pass # TODO

    def timer_button_clicked(self) -> None:
        pass # TODO

    def hide_button_clicked(self) -> None:
        self.parent.widget_switch_animation(widget=self)

    class TimeSlider(QtWidgets.QFrame):
        pass # TODO
