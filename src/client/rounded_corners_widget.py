from PySide6 import QtWidgets, QtCore, QtGui


class RoundedCornersWindow(QtWidgets.QWidget):
    def __init__(self):
        super(RoundedCornersWindow, self).__init__()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#232323")))
        pen = QtGui.QPen(QtGui.QColor('#282828'))
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect(), 15, 15)  # Радиус закругления углов
