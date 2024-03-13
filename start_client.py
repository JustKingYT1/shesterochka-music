from src.client.main_window import MainWindow
from PySide6 import QtWidgets
import sys


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec()