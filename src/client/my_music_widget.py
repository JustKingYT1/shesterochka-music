from PySide6 import QtWidgets, QtCore, QtGui


class MyMusicMenu(QtWidgets.QWidget):
    stop_flag: bool = False
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        pass

    def __setting_ui(self) -> None:
        pass