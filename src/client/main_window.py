from PySide6 import QtWidgets, QtCore, QtGui
import sys
from src.client.side_menu_widget import SideMenu
from src.client.settings_widget import SettingsMenu
from src.client.tools.session import Session
from src.client.animated_panel_widget import AnimatedPanel


class MainWindow(QtWidgets.QMainWindow):
    session: Session = Session() # type: ignore
    opened_widget: AnimatedPanel = None
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
        self.animated_widgets = [self.settings_menu, self.settings_menu.register_dialog, self.settings_menu.login_dialog]

    def __setting_ui(self) -> None:
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_v_layout)
        self.resize(400, 500)
        self.session.set_parent(self)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)
        self.main_v_layout.addWidget(self.side_menu)
        self.side_menu.group_buttons.buttonClicked.connect(lambda button: self.__button_clicked(button))

    def show_message(self, text: str, parent=None, error: bool=False):
        message_box = QtWidgets.QMessageBox(parent if parent else self)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information if not error else QtWidgets.QMessageBox.Icon.Critical)
        message_box.setText(text)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()

    def hide_opened_widgets(self, widget) -> None:
        for widget in self.animated_widgets:
            if widget.isVisible() and widget != self.opened_widget:
                widget.start_animation()

    def __button_clicked(self, button: QtWidgets.QToolButton) -> None:
        widget = None

        if button.objectName() == 'main_page':
            widget = self
        elif button.objectName() == 'my_music':
            widget = self
        elif button.objectName() == 'settings':
            widget = self.settings_menu

        self.hide_opened_widgets(widget)
        widget.start_animation()
        widget.raise_()
        self.opened_widget = widget
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    app.exec()