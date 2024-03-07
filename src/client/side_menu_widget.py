from PySide6 import QtWidgets, QtCore, QtGui


class SideMenu(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.group_buttons = QtWidgets.QButtonGroup()
        self.main_page_button = QtWidgets.QToolButton()
        self.my_music_button = QtWidgets.QToolButton()
        self.settings_button = QtWidgets.QToolButton()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        # self.main_h_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_h_layout.addWidget(self.main_page_button)
        self.main_h_layout.addWidget(self.my_music_button)
        self.main_h_layout.addWidget(self.settings_button)

        self.main_page_button.setObjectName('main_page')
        self.my_music_button.setObjectName('my_music')
        self.settings_button.setObjectName('settings')

        self.group_buttons.addButton(self.main_page_button)
        self.group_buttons.addButton(self.my_music_button)
        self.group_buttons.addButton(self.settings_button)

        # self.main_page_button.resize(24, 24)
        # self.my_music_button.resize(24, 24)
        # self.settings_button.resize(24, 24)