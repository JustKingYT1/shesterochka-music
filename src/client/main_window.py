from PySide6 import QtWidgets, QtCore, QtGui, QtMultimedia
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
    media_player: QtMultimedia.QMediaPlayer = QtMultimedia.QMediaPlayer()
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
        self.my_music_menu = None
        self.timer = QtCore.QTimer(self)
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

        self.main_page_menu.set_button(self.side_menu.main_page_button)
        # self.my_music_menu.set_button(self.side_menu.my_music_button)
        self.settings_menu.set_button(self.side_menu.settings_button)

        self.main_v_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_v_layout.addWidget(self.side_menu, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_menu.group_buttons.buttonClicked.connect(lambda button: self.button_clicked(button))

    def show_message(self, text: str, parent=None, error: bool=False):
        message_box = QtWidgets.QMessageBox(parent if parent else self)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information if not error else QtWidgets.QMessageBox.Icon.Critical)
        message_box.setText(text)
        #https://youtu.be/xwGvW600e2c?si=2H9NRwteRmZOFYrc
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        message_box.exec()
    
    def widget_switch_animation(self, button) -> None:
        if self.opened_widget: 
            if self.opened_widget != button.widget:
                self.timer.singleShot(320, lambda button=button: self.on_timer_finished(button))
                self.start_widget_animation(self.opened_widget)
            elif self.opened_widget == button.widget:
                self.start_widget_animation(button.widget)
        else:
            self.start_widget_animation(button.widget)
    
    def start_widget_animation(self, widget: AnimatedPanel) -> None:
        if widget.button:
            widget.button.toggle_pressed()
        widget.start_animation()
        widget.raise_()
        self.opened_widget = widget

    def on_timer_finished(self, button) -> None:
        self.start_widget_animation(button.widget)

    def button_clicked(self, button) -> None:
        self.widget_switch_animation(button)

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    app.exec()
    # ВАДЕМ ВАГИН