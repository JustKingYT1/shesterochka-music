from PySide6 import QtWidgets, QtCore, QtGui
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.pixmap_tools import get_pixmap
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.dialog_widgets.register_dialog_widget import RegisterDialog
from src.client.dialog_widgets.login_dialog_widget import LoginDialog
from src.client.side_menu_widget import SideMenu


class SettingsMenu(AnimatedPanel):
    def __init__(self, parent):
        super(SettingsMenu, self).__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.setting_dialog_button = SideMenu.SideButton(self, 'settings', QtCore.QSize(19, 19))
        self.authorize_v_layout = QtWidgets.QVBoxLayout()
        self.user_profile_layout = QtWidgets.QVBoxLayout()
        self.register_dialog = RegisterDialog(self.parent)
        self.login_dialog = LoginDialog(self.parent)
        self.spacer = QtWidgets.QSpacerItem(0, 100)
        self.settings_dialog = SettingsMenu.SettingsDialog(self)
        self.user_nickname_label = QtWidgets.QLabel('Гость')
        self.user_image_label = QtWidgets.QLabel('Пользователь')
        self.log_in_button = QtWidgets.QPushButton('Войти')
        self.register_label = QtWidgets.QLabel('<a href=register_button>Зарегистрироваться?</a>')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setObjectName('SettingsMenu')
        self.main_v_layout.setContentsMargins(5, 5, 5, 5)
        set_style_sheet_for_widget(self, 'settings_menu.qss')

        self.main_v_layout.addWidget(self.scroll_area)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.verticalScrollBar().setMaximumWidth(0)
        self.scroll_area.verticalScrollBar().setObjectName('ScrollBar')

        self.log_in_button.setObjectName('LoginButton')
        self.register_label.setObjectName('RegisterLabel')

        self.scroll_widget.setObjectName('ScrollWidget')
        self.scroll_area.setObjectName('ScrollArea')
    
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.user_image_label.setFixedSize(128, 128)
        self.user_image_label.setPixmap(get_pixmap('user_undefined.png'))

        self.setting_dialog_button.setFixedSize(24, 24)

        self.register_label.setOpenExternalLinks(False)
        self.register_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)

        self.register_label.linkActivated.connect(self.register_label_clicked)
        self.setting_dialog_button.clicked.connect(self.settings_dialog_button_clicked)
        self.log_in_button.clicked.connect(self.login_button_clicked)
        self.setting_dialog_button.hide()

        self.scroll_layout.addWidget(self.setting_dialog_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        self.user_profile_layout.addWidget(self.user_image_label, 0)
        
        self.user_profile_layout.addWidget(self.user_nickname_label, 1, QtCore.Qt.AlignmentFlag.AlignTop)

        self.user_profile_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.scroll_layout.addLayout(self.user_profile_layout)

        self.scroll_layout.addSpacing(120)

        self.authorize_v_layout.addWidget(self.log_in_button)
        self.authorize_v_layout.addWidget(self.register_label)

        self.authorize_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.scroll_layout.addLayout(self.authorize_v_layout)

    def register_label_clicked(self, _) -> None:
        self.open_register_dialog()

    def login_button_clicked(self) -> None:
        self.open_login_dialog()

    def open_register_dialog(self) -> None:
        self.parent.widget_switch_animation(widget=self.register_dialog)

    def open_login_dialog(self) -> None:
        self.parent.widget_switch_animation(widget=self.login_dialog)

    def authorize_action(self) -> None:
        self.user_nickname_label.setText(self.parent.session.user.nickname)
        self.log_in_button.hide()
        self.register_label.hide()
        self.setting_dialog_button.show()
        self.main_v_layout.addSpacerItem(self.spacer)

        self.parent.main_page_menu.update_music(True)
        self.parent.my_music_menu.reload_widget(self.parent.my_music_menu.main_v_layout)
        self.parent.my_music_menu.update_music(True)
        self.parent.deleted_music_menu.update_music(True)

        self.size_expand()

    def settings_dialog_button_clicked(self) -> None:
        self.setting_dialog_button.toggle_pressed()
        self.settings_dialog.toggle_widget()
        self.settings_dialog.raise_()

    def exit_account(self) -> None:
        self.parent.session.leave()
        self.user_nickname_label.setText(self.parent.session.user.nickname)
        self.log_in_button.show()
        self.register_label.show()
        self.setting_dialog_button.hide()
        self.main_v_layout.removeItem(self.spacer)

        self.parent.main_page_menu.update_music(True)
        self.parent.my_music_menu.reload_widget(self.parent.my_music_menu.main_v_layout)

        self.parent.music_info_widget.like_button.pressed = False
        self.parent.music_info_widget.like_button.toggle_pressed()
        self.parent.current_music_widget.like_button.pressed = False
        self.parent.current_music_widget.like_button.toggle_pressed()
        self.parent.deleted_music_menu.update_music(True)

        self.parent.widget_switch_animation(self.button)
        self.size_expand()

    class SettingsDialog(QtWidgets.QFrame):
        is_visible: bool = False
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent = parent
            self.__init_ui()
            self.__setting_ui()
            self.hide()
        
        def __init_ui(self) -> None:
            self.main_v_layout = QtWidgets.QVBoxLayout(self)
            self.exit_button = QtWidgets.QToolButton(self)
            self.section_deleted_music = QtWidgets.QToolButton(self)
            self.animation = QtCore.QPropertyAnimation(self, b"geometry")

        def __setting_ui(self) -> None:
            self.setLayout(self.main_v_layout)
            self.setObjectName('SettingsDialog')
            set_style_sheet_for_widget(self, 'settings_dialog.qss')
            self.setFixedWidth(self.parent.setting_dialog_button.sizeHint().width())
            self.resize(self.width(), self.parent.setting_dialog_button.sizeHint().height())
            
            self.main_v_layout.setContentsMargins(0, 0, 0, 0)
            self.main_v_layout.addWidget(self.section_deleted_music)
            self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 7))
            self.main_v_layout.addWidget(self.exit_button)

            self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            self.section_deleted_music.setIcon(get_pixmap('deleted_playlist.png'))
            self.section_deleted_music.setIconSize(QtCore.QSize(18, 18))

            self.exit_button.setIcon(get_pixmap('logout.png'))
            self.exit_button.setIconSize(QtCore.QSize(18, 18))

            self.animation.setDuration(300)
            self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutQuad)
            self.animation.finished.connect(self.onAnimationFinished)

            self.section_deleted_music.clicked.connect(self.open_section_deleted_music)
            self.exit_button.clicked.connect(self.exit_button_clicked)

        def show_widget(self):
            self.show()
            button_geometry = self.parent.setting_dialog_button.geometry()
            button_center_x = button_geometry.left() + (button_geometry.width() - 5)
            start_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom() + 8, self.width(), 0)
            end_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom() + 8, self.width(), 90)
            self.setGeometry(start_rect)
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            self.animation.start()
            self.is_visible = not self.is_visible

        def hide_widget(self):
            button_geometry = self.parent.setting_dialog_button.geometry()
            button_center_x = button_geometry.left() + (button_geometry.width() - 5)
            start_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom(), self.width(), self.height())
            end_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom(), self.width(), 0)
            self.animation.setStartValue(start_rect)
            self.animation.setEndValue(end_rect)
            self.animation.start()
            self.is_visible = not self.is_visible
        
        def open_section_deleted_music(self) -> None:
            self.parent.parent.widget_switch_animation(widget=self.parent.parent.deleted_music_menu)

        def toggle_widget(self) -> None:
            if not self.is_visible:
                self.show_widget()
            else: 
                self.hide_widget()

        def exit_button_clicked(self) -> None:
            self.toggle_widget()
            self.parent.exit_account()

        def onAnimationFinished(self):
            if self.animation.state() == QtCore.QPropertyAnimation.State.Stopped and not self.is_visible:
                self.hide()
