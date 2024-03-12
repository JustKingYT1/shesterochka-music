from PySide6 import QtWidgets, QtCore, QtGui
import sys
from src.client.side_menu_widget import SideMenu
from src.client.settings_widget import SettingsMenu
from src.client.tools.session import Session
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.pixmap_tools import get_pixmap
from src.client.main_page_widget import MainPageMenu
from src.client.tools.style_setter import set_style_sheet_for_widget


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
        self.logo_label = QtWidgets.QLabel()
        self.settings_menu = SettingsMenu(self)
        self.main_page_menu = MainPageMenu(self)
        self.side_menu = SideMenu(self)
        self.animated_widgets = [self.settings_menu, 
                                 self.settings_menu.register_dialog, 
                                 self.settings_menu.login_dialog, 
                                 self.main_page_menu]

    def __setting_ui(self) -> None:
        self.setCentralWidget(self.central_widget)
        self.setObjectName('MainWindow')
        set_style_sheet_for_widget(self, 'main_window.qss')
        self.central_widget.setLayout(self.main_v_layout)
        self.resize(400, 500)
        self.session.set_parent(self)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_label.setFixedSize(256, 256)

        self.main_v_layout.addSpacing(100)

        self.logo_label.setPixmap(get_pixmap('logo_256px.png'))

        self.main_page_menu.size_expand()

        self.side_menu.main_page_button.set_widget(self.main_page_menu)
        self.side_menu.my_music_button.set_widget(self)
        self.side_menu.settings_button.set_widget(self.settings_menu)

        self.main_v_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.side_menu, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_menu.group_buttons.buttonClicked.connect(lambda button: self.__button_clicked(button))

    def show_message(self, text: str, parent=None, error: bool=False):
        message_box = QtWidgets.QMessageBox(parent if parent else self)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information if not error else QtWidgets.QMessageBox.Icon.Critical)
        message_box.setText(text)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()

    def __button_clicked(self, button) -> None:
        button.toggle_pressed()
        if self.opened_widget:
            self.opened_widget.start_animation() if self.opened_widget != button.widget else None
        button.widget.start_animation()
        button.widget.raise_()
        self.opened_widget = button.widget
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    app.exec()
    # ВАДЕМ ВАГИН