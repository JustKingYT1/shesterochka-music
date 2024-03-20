from PySide6 import QtWidgets, QtCore, QtGui
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.pixmap_tools import get_pixmap
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.dialog_widgets.register_dialog_widget import RegisterDialog
from src.client.dialog_widgets.login_dialog_widget import LoginDialog
import settings
import eyed3


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
        self.exit_button = QtWidgets.QToolButton()
        self.authorize_v_layout = QtWidgets.QVBoxLayout()
        self.user_profile_layout = QtWidgets.QVBoxLayout()
        self.register_dialog = RegisterDialog(self.parent)
        self.login_dialog = LoginDialog(self.parent)
        self.spacer = QtWidgets.QSpacerItem(0, 100)
        self.user_nickname_label = QtWidgets.QLabel('Гость')
        self.user_image_label = QtWidgets.QLabel('Пользователь')
        self.log_in_button = QtWidgets.QPushButton('Войти')
        self.register_label = QtWidgets.QLabel('<a href=register_button>Зарегистрироваться?</a>')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setObjectName('SettingsMenu')
        self.main_v_layout.setContentsMargins(10, 10, 10, 10)
        set_style_sheet_for_widget(self, 'settings_menu.qss')

        self.main_v_layout.addWidget(self.scroll_area)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0,0,0,0)

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

        self.exit_button.setFixedSize(24, 24)

        self.register_label.setOpenExternalLinks(False)
        self.register_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)

        self.register_label.linkActivated.connect(self.register_label_clicked)
        self.exit_button.clicked.connect(self.exit_button_clicked)
        self.log_in_button.clicked.connect(self.login_button_clicked)
        self.exit_button.hide()

        self.exit_button.setIcon(get_pixmap('cancel.png'))

        self.scroll_layout.addWidget(self.exit_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        self.user_profile_layout.addWidget(self.user_image_label)
        
        self.user_profile_layout.addWidget(self.user_nickname_label)

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
        self.exit_button.show()
        self.main_v_layout.addSpacerItem(self.spacer)
        self.parent.my_music_menu.reload_widget()
        self.size_expand()

    def exit_button_clicked(self) -> None:
        self.exit_account()

    def exit_account(self) -> None:
        self.parent.session.leave()
        self.user_nickname_label.setText(self.parent.session.user.nickname)
        self.log_in_button.show()
        self.register_label.show()
        self.exit_button.hide()
        self.main_v_layout.removeItem(self.spacer)
        self.parent.main_page_menu.reload_widget()
        self.parent.my_music_menu.reload_widget()
        self.parent.music_info_widget.like_button.pressed = False
        self.parent.music_info_widget.like_button.toggle_pressed()

        self.start_animation()
        self.size_expand()
