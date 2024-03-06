from PySide6 import QtWidgets, QtCore, QtGui
from settings import IMG_DIR


def get_pixmap(name: str) -> QtGui.QPixmap:
    return QtGui.QPixmap(f'{IMG_DIR}/{name}')