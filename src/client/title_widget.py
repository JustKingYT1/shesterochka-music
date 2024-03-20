from PySide6 import QtWidgets, QtCore, QtGui
from src.client.tools.pixmap_tools import get_pixmap
from src.client.tools.style_setter import set_style_sheet_for_widget


class TitleWidget(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.title_layout = QtWidgets.QHBoxLayout()
        self.exit_button = QtWidgets.QPushButton()
        self.curtail_button = QtWidgets.QPushButton()
        self.size_expand_button = QtWidgets.QPushButton()
        self.window_icon = QtWidgets.QToolButton()
        self.window_title = QtWidgets.QLabel('Title')

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.main_h_layout.setContentsMargins(5,2,5,2.5)
        self.setObjectName('TitleWidget')

        set_style_sheet_for_widget(self, 'title_widget.qss')

        self.button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.title_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.title_layout.addWidget(self.window_icon)
        self.title_layout.addWidget(self.window_title)
        self.button_layout.addWidget(self.curtail_button)
        self.button_layout.addWidget(self.size_expand_button)
        self.button_layout.addWidget(self.exit_button)

        self.main_h_layout.addLayout(self.title_layout)
        self.main_h_layout.addLayout(self.button_layout)

        self.size_expand_button.setEnabled(False)

        self.exit_button.setFixedSize(18, 18)
        self.size_expand_button.setFixedSize(18, 18)
        self.curtail_button.setFixedSize(18, 18)

        self.exit_button.setIcon(get_pixmap('exit'))
        self.size_expand_button.setIcon(get_pixmap('size_expand'))
        self.curtail_button.setIcon(get_pixmap('curtail'))

        self.exit_button.setIconSize(QtCore.QSize(18, 18))
        self.size_expand_button.setIconSize(QtCore.QSize(18, 18))
        self.curtail_button.setIconSize(QtCore.QSize(18, 18))

        self.exit_button.clicked.connect(self.exit_button_clicked)
        self.curtail_button.clicked.connect(self.curtail_button_clicked)

    def exit_button_clicked(self) -> None:
        self.parent.main_page_menu.stop_flag = True
        self.parent.my_music_menu.stop_flag = True
        exit()

        exit()

    def curtail_button_clicked(self) -> None:
        self.parent.showMinimized()

    def set_window_title(self, text: str) -> None:
        self.window_title.setText(text)

    def set_window_icon(self, title: str) -> None:
        icon = get_pixmap(title)
        self.window_icon.setFixedSize(QtCore.QSize(20, 20))
        self.window_icon.setIcon(icon)
        self.window_icon.setIconSize(QtCore.QSize(20, 20))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.parent.move(event.globalPos() - self.offset)
        