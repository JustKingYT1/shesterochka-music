from PySide6 import QtWidgets, QtCore, QtGui
import sys
from src.database_models import UserPlaylists
from src.client.side_menu_widget import SideMenu
from src.client.settings_widget import SettingsMenu
from src.client.tools.session import Session
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.pixmap_tools import get_pixmap
from src.client.main_page_widget import MainPageMenu, TypesMenu
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.tools.config_manager import ConfigManager
from src.client.music_info_widget import MusicInfo
from src.client.music_session import MusicSession
from src.client.title_widget import TitleWidget
from src.client.rounded_corners_widget import RoundedCornersWindow
import settings
import eyed3

class MainWindow(QtWidgets.QMainWindow):
    session: Session = Session() # type: ignore
    music_session: MusicSession = None
    opened_widget: AnimatedPanel = None
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.__init_ui()
        self.__setting_ui()
        self.show()
    
    def __init_ui(self) -> None:
        self.central_widget = RoundedCornersWindow()
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.container_layout = QtWidgets.QVBoxLayout()
        self.music_session = MusicSession(self)
        self.title_widget = TitleWidget(self)
        self.logo_label = QtWidgets.QPushButton()
        self.side_menu = SideMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.main_page_menu = MainPageMenu(self, TypesMenu.MainMusic, 0)   
        self.my_music_menu = MainPageMenu(self, TypesMenu.MyMusic, 1)
        self.music_info_widget = MusicInfo(self, eyed3.load(f'{settings.MUSIC_DIR}/empty.mp3'))
        self.timer = QtCore.QTimer(self)

    def __setting_ui(self) -> None:
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  
        self.setWindowIcon(get_pixmap('logo'))
        self.setWindowTitle('Shesterocka Music')
        self.setCentralWidget(self.central_widget)
        self.setObjectName('MainWindow')
        
        self.main_page_menu.update_music()
        self.my_music_menu.update_music()

        set_style_sheet_for_widget(self, 'main_window.qss')

        self.set_user()

        self.title_widget.set_window_title('Shesterocka Music')
        self.title_widget.set_window_icon('logo')

        self.central_widget.setLayout(self.main_v_layout)
        self.setFixedSize(400, 550)
        self.session.set_parent(self)

        self.main_v_layout.addWidget(self.title_widget) 
        self.main_v_layout.addLayout(self.container_layout)

        self.main_v_layout.setContentsMargins(0,0,0,0)
        self.container_layout.setContentsMargins(10, 10, 10, 10)

        self.logo_label.setFixedSize(128, 128)

        self.container_layout.addSpacing(70)

        self.logo_label.setFixedSize(QtCore.QSize(168, 168))

        pixmap = get_pixmap('logo1')

        self.logo_label.setIcon(pixmap)
        self.logo_label.setIconSize(QtCore.QSize(168, 168))

        self.side_menu.main_page_button.set_widget(self.main_page_menu)
        self.side_menu.my_music_button.set_widget(self.my_music_menu)
        self.side_menu.settings_button.set_widget(self.settings_menu)

        self.main_page_menu.set_button(self.side_menu.main_page_button)
        self.my_music_menu.set_button(self.side_menu.my_music_button)
        self.settings_menu.set_button(self.side_menu.settings_button)

        self.container_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.music_info_widget, 1, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.side_menu, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_menu.group_buttons.buttonClicked.connect(lambda button: self.button_clicked(button))
    
    def show_message(self, text: str, parent=None, error: bool=False):
        message_box = QtWidgets.QMessageBox(parent if parent else self)
        message_box.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        message_box.setIcon(QtWidgets.QMessageBox.Icon.Information if not error else QtWidgets.QMessageBox.Icon.Critical)
        message_box.setText(text)
        message_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        set_style_sheet_for_widget(message_box, 'message_box.qss')
        message_box.buttons()[0].setFixedSize(60, 20)
        
        message_box.exec()
    
    def set_user(self) -> None:
        config = ConfigManager.get_config()

        if config['user']['id'] != -1:
            self.settings_menu.login_dialog.nickname_line_edit.setText(config['user']['login'])
            self.settings_menu.login_dialog.password_line_edit.setText(config['user']['password'])
            self.settings_menu.login_dialog.login_button_clicked(not_message_box=True)

    def change_current_music_widget_style(self) -> None:
        if not self.music_session.hasAudio():
            self.music_info_widget.play_button.setEnabled(True)
            self.music_info_widget.like_button.setEnabled(True)
        if self.music_session.widget:
            if self.music_session.widget.toggle:
                self.music_session.widget.toggle_pressed()
    
    def change_state_like_button(self) -> None:
        if not self.music_info_widget.like_button.pressed:
            self.music_info_widget.like_button.toggle_pressed()
        self.music_info_widget.like_button.toggle_pressed() if UserPlaylists.get_or_none((UserPlaylists.user_id==self.session.user.id) & \
                                                                (UserPlaylists.music_id == self.music_info_widget.music.tag.id)) else None

    def widget_switch_animation(self, button=None, widget=None) -> None:
        if self.opened_widget: 
            if not self.opened_widget.isVisible():
                self.opened_widget = button.widget if button else widget
            if self.opened_widget != (widget if not button else button.widget):
                self.start_widget_animation(self.opened_widget)
                self.timer.singleShot(320, lambda button=button: self.on_timer_finished(button.widget if button else widget))
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

    def on_timer_finished(self, widget) -> None:
        self.start_widget_animation(widget)

    def button_clicked(self, button) -> None:
        self.widget_switch_animation(button)
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = MainWindow()
    app.exec()