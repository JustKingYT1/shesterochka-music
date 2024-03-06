from PySide6 import QtWidgets, QtCore, QtGui
import sys
from src.client.side_menu_widget import SideMenu
from src.client.settings_widget import SettingsMenu


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.__init_ui()
        self.__setting_ui()
        self.show()
    
    def __init_ui(self) -> None:
        self.central_widget = QtWidgets.QWidget()
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.settings_menu = SettingsMenu(self)
        self.side_menu = SideMenu(self)

    def __setting_ui(self) -> None:
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_v_layout)
        self.resize(400, 500)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_layout.addWidget(self.side_menu)
        self.side_menu.settings_button.clicked.connect(self.__button_clicked)

    def __button_clicked(self) -> None:
        self.settings_menu.start_animation()
        self.settings_menu.raise_()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    app.exec()