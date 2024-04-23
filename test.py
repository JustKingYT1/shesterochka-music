import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QToolButton, QFrame
from PySide6.QtCore import QSize, QPoint, QRect, QPropertyAnimation, QEasingCurve

class PopupSettingsDialog(QFrame):
    is_visible: bool = False
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: gray; border: 1px solid black; border-radius: 5px;")
        self.setFixedWidth(parent.button.width())
        self.resize(self.width(), parent.button.height() * 3)  # Ширина как у кнопки
        self.setParent(parent)
        self.hide()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)
        self.button1 = QToolButton(self)
        layout.addWidget(self.button1)
        self.button2 = QToolButton(self)
        layout.addWidget(self.button2)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.finished.connect(self.onAnimationFinished)

    def show_widget(self):
        self.show()
        start_rect = QRect(self.parent().button.geometry().bottomLeft(), QSize(self.width(), 0))
        end_rect = QRect(self.parent().button.geometry().bottomLeft(), QSize(self.width(), 90))
        self.setGeometry(start_rect)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        self.is_visible = not self.is_visible
    
    def toggle_widget(self) -> None:
        if not self.is_visible:
            self.show_widget()
        else: 
            self.hide_widget()

    def hide_widget(self):
        start_rect = QRect(self.parent().button.geometry().bottomLeft(), QSize(self.width(), self.height()))
        end_rect = QRect(self.parent().button.geometry().bottomLeft(), QSize(self.width(), 0))

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        self.is_visible = not self.is_visible

    def onAnimationFinished(self):
        if self.animation.state() == QPropertyAnimation.State.Stopped and not self.is_visible:
            self.hide()

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(400, 500)

        self.button = QToolButton(self)
        self.button.setFixedSize(24, 24)
        self.button.clicked.connect(self.togglePopup)

        self.popupWidget = PopupSettingsDialog(self)

        self.main_h_layout = QtWidgets.QHBoxLayout()

        self.setLayout(self.main_h_layout)

        self.main_h_layout.addWidget(self.popupWidget, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

    def togglePopup(self):
        self.popupWidget.toggle_widget()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWidget()
    mainWindow.show()
    sys.exit(app.exec_())
