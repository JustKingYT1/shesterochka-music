from PySide6 import QtWidgets, QtCore, QtGui
import sys
from animated_panel import AnimatedPanel


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.__init_ui()
        self.__setting_ui()
        self.show()
    
    def __init_ui(self) -> None:
        self.central_widget = QtWidgets.QWidget()
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.animated_panel = AnimatedPanel(self)
        self.button = QtWidgets.QPushButton()

    def __setting_ui(self) -> None:
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_h_layout)
        self.main_h_layout.addWidget(self.button)
        self.button.setFixedSize(20, 20)
        self.button.clicked.connect(self.__button_clicked)

    def __button_clicked(self) -> None:
        self.animated_panel.start_animation()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    app.exec()