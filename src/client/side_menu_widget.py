from PySide6 import QtWidgets, QtCore, QtGui
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.client.tools.pixmap_tools import get_pixmap
from src.client.animated_panel_widget import AnimatedPanel


class SideMenu(QtWidgets.QFrame):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(SideMenu, self).__init__(parent)
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.group_buttons = QtWidgets.QButtonGroup()
        icon_size = QtCore.QSize(20, 20)
        self.main_page_button = SideMenu.SideButton(self, 'main_music', icon_size)
        self.my_music_button = SideMenu.SideButton(self, 'my_music', icon_size)
        self.settings_button = SideMenu.SideButton(self, 'account', icon_size)

    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        
        self.setObjectName('SideMenu')

        set_style_sheet_for_widget(self, 'side_menu.qss')

        self.main_h_layout.setContentsMargins(5, 5, 5, 5)
        
        self.main_h_layout.addWidget(self.main_page_button)
        self.main_h_layout.addWidget(self.my_music_button)
        self.main_h_layout.addWidget(self.settings_button)

        self.main_page_button.setObjectName('main_page')
        self.my_music_button.setObjectName('my_music')
        self.settings_button.setObjectName('settings')

        self.group_buttons.addButton(self.main_page_button)
        self.group_buttons.addButton(self.my_music_button)
        self.group_buttons.addButton(self.settings_button)

    class SideButton(QtWidgets.QToolButton):
        pixmap_name: str
        pressed: bool = False
        widget: AnimatedPanel = None

        def __init__(self, 
                     parent: QtWidgets.QWidget, 
                     pixmap_name: str, 
                     size: QtCore.QSize) -> None:
            super(SideMenu.SideButton, self).__init__(parent)
            self.pixmap_name = pixmap_name
            self.setFixedSize(size)
            self.setIcon(get_pixmap(pixmap_name))
            self.setIconSize(size)

        def set_widget(self, widget: AnimatedPanel):
            self.widget = widget

        def toggle_pressed(self) -> None:
            self.pressed = not self.pressed
            self.setIcon(
                get_pixmap(f"{self.pixmap_name}{'_pressed' if not self.pressed else ''}.png")
            )
