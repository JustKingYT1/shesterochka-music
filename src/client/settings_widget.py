from PySide6 import QtWidgets, QtCore, QtGui
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.pixmap_tools import get_pixmap


class SettingsMenu(AnimatedPanel):
    def __init__(self, parent):
        super(SettingsMenu, self).__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.exit_button = QtWidgets.QToolButton()
        self.authorize_v_layout = QtWidgets.QVBoxLayout()
        self.user_profile_layout = QtWidgets.QVBoxLayout()
        self.user_name_label = QtWidgets.QLabel('Гость')
        self.user_nickname_label = QtWidgets.QLabel('Гость')
        self.user_image_label = QtWidgets.QLabel('Пользователь')
        self.log_in_button = QtWidgets.QPushButton('Войти')
        self.register_label = QtWidgets.QLabel('<a href=register_button>Зарегистрироваться?</a>')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.setContentsMargins(10, 10, 10, 10)
        
        self.user_image_label.setFixedSize(128, 128)
        self.user_image_label.setPixmap(get_pixmap('user_undefined.png'))

        self.register_label.setOpenExternalLinks(False)
        self.register_label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)

        self.register_label.linkActivated.connect(self.register_label_clicked)

        self.main_v_layout.addWidget(self.exit_button, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)
        self.user_profile_layout.addWidget(self.user_image_label)
        self.user_profile_layout.addWidget(self.user_name_label)
        self.user_profile_layout.addWidget(self.user_nickname_label)

        self.user_profile_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.main_v_layout.addLayout(self.user_profile_layout)

        self.main_v_layout.addSpacing(100)

        self.authorize_v_layout.addWidget(self.log_in_button)
        self.authorize_v_layout.addWidget(self.register_label)

        self.authorize_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addLayout(self.authorize_v_layout)
    
    def register_label_clicked(self, link) -> None:
        if link == 'register_button':
            print(1)