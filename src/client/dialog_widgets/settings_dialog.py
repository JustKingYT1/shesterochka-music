from PySide6 import QtWidgets, QtCore, QtGui
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.tools.pixmap_tools import get_pixmap


class SettingsDialog(QtWidgets.QFrame):
    is_visible: bool = False
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()
        self.hide()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout(self)
        self.exit_button = QtWidgets.QToolButton(self)
        self.section_deleted_music = QtWidgets.QToolButton(self)
        self.animation = QtCore.QPropertyAnimation(self, b"geometry")

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.setObjectName('SettingsDialog')
        set_style_sheet_for_widget(self, 'settings_dialog.qss')
        self.setFixedWidth(self.parent.setting_dialog_button.sizeHint().width())
        self.resize(self.width(), self.parent.setting_dialog_button.sizeHint().height())
        
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.addWidget(self.section_deleted_music)
        self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 7))
        self.main_v_layout.addWidget(self.exit_button)

        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.section_deleted_music.setIcon(get_pixmap('deleted_playlist.png'))
        self.section_deleted_music.setIconSize(QtCore.QSize(18, 18))

        self.exit_button.setIcon(get_pixmap('logout.png'))
        self.exit_button.setIconSize(QtCore.QSize(18, 18))

        self.animation.setDuration(300)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutQuad)
        self.animation.finished.connect(self.onAnimationFinished)

        self.exit_button.clicked.connect(self.exit_button_clicked)

    def show_widget(self):
        self.show()
        button_geometry = self.parent.setting_dialog_button.geometry()
        button_center_x = button_geometry.left() + (button_geometry.width() - 5)
        start_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom() + 8, self.width(), 0)
        end_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom() + 8, self.width(), 90)
        self.setGeometry(start_rect)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        self.is_visible = not self.is_visible

    def hide_widget(self):
        button_geometry = self.parent.setting_dialog_button.geometry()
        button_center_x = button_geometry.left() + (button_geometry.width() - 5)
        start_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom(), self.width(), self.height())
        end_rect = QtCore.QRect(button_center_x - self.width() / 2, button_geometry.bottom(), self.width(), 0)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        self.is_visible = not self.is_visible

    def toggle_widget(self) -> None:
        if not self.is_visible:
            self.show_widget()
        else: 
            self.hide_widget()

    def exit_button_clicked(self) -> None:
        self.toggle_widget()
        self.parent.exit_account()

    def onAnimationFinished(self):
        if self.animation.state() == QtCore.QPropertyAnimation.State.Stopped and not self.is_visible:
            self.hide()
