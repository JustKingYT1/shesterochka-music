from PySide6 import QtCore, QtWidgets, QtGui
from src.client.animated_panel_widget import AnimatedPanel
from src.client.tools.pixmap_tools import get_pixmap
from src.client.tools.style_setter import set_style_sheet_for_widget
from src.database_models import UserModel


class RegisterDialog(AnimatedPanel):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.__init_ui()
        self.__setting_ui()

    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()

        self.register_values_layout = QtWidgets.QHBoxLayout()

        self.label_layout = QtWidgets.QVBoxLayout()
        self.line_edit_layout = QtWidgets.QVBoxLayout()

        self.logo_label = QtWidgets.QLabel()

        self.title_label = QtWidgets.QLabel('<H1>Регистрация</H1>')

        self.nickname_label = QtWidgets.QLabel('Никнейм: ')
        self.password_label = QtWidgets.QLabel('Пароль: ')
        self.confirm_label = QtWidgets.QLabel('Подтверждение пароля: ')

        self.nickname_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit = QtWidgets.QLineEdit()
        self.confirm_line_edit = QtWidgets.QLineEdit()

        self.register_button = QtWidgets.QPushButton('Подтвердить')
        self.cancel_button = QtWidgets.QToolButton()

    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)

        self.setObjectName('RegisterDialog')

        set_style_sheet_for_widget(self, 'register_dialog.qss')

        self.main_v_layout.setContentsMargins(10, 10, 10, 10)

        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.main_v_layout.addWidget(self.cancel_button, 1, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

        self.register_values_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)

        self.logo_label.setFixedSize(128, 128)

        self.logo_label.setPixmap(get_pixmap('logo_126px.png'))
        self.cancel_button.setIcon(get_pixmap('exit_reversed.png'))

        self.logo_label.setObjectName('LogoLabel')

        self.main_v_layout.addWidget(self.logo_label, 1, QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 35))
        self.main_v_layout.addWidget(self.title_label,1, QtCore.Qt.AlignmentFlag.AlignCenter| QtCore.Qt.AlignmentFlag.AlignTop)

        self.main_v_layout.addSpacerItem(QtWidgets.QSpacerItem(0, 35))

        self.main_v_layout.addLayout(self.register_values_layout, 2)

        self.register_values_layout.addLayout(self.label_layout)
        self.register_values_layout.addLayout(self.line_edit_layout)

        self.label_layout.addWidget(self.nickname_label)
        self.line_edit_layout.addWidget(self.nickname_line_edit)

        self.label_layout.addWidget(self.password_label)
        self.line_edit_layout.addWidget(self.password_line_edit)

        self.label_layout.addWidget(self.confirm_label)
        self.line_edit_layout.addWidget(self.confirm_line_edit)

        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirm_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.main_v_layout.addWidget(self.register_button, 3, QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTop)
        
        self.register_button.clicked.connect(self.register_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_button_clicked)

    def validate_text_line_edits(self) -> bool:
        if self.confirm_line_edit.text() != self.password_line_edit.text():
            return False
        
        for x in (self.nickname_line_edit, self.password_line_edit, self.confirm_line_edit):
            if x.text() == '':
                return False
            
        return True

    def register_button_clicked(self) -> None:
        if not self.validate_text_line_edits():
            self.parent.show_message(text='One or more fields is empty, or confirm password incorrect', 
                                     error=True, 
                                     parent=self)
            return
        
        self.parent.session.register(UserModel(
            nickname=self.nickname_line_edit.text(),
            password=self.password_line_edit.text()
        ))

        if self.parent.session.auth:
            self.parent.show_message(text='Succesfully register')
        else:
            return

        self.parent.settings_menu.authorize_action()

        self.cancel_button_clicked()
    
    def cancel_button_clicked(self) -> None:
        self.parent.widget_switch_animation(self.parent.side_menu.settings_button)
