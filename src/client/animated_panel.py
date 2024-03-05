from PySide6 import QtWidgets, QtCore, QtGui


class AnimatedPanel(QtWidgets.QFrame):
    is_opened: bool = False
    main_v_layout: QtWidgets.QVBoxLayout = None
    animator_pos: QtCore.QPropertyAnimation = None
    animator_size: QtCore.QPropertyAnimation = None
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(AnimatedPanel, self).__init__(parent)
        self.parent: QtWidgets.QMainWindow = parent
        self.__init_ui()
        self.__setting_ui()
        self.hide()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QVBoxLayout()
        self.animation_size = QtCore.QPropertyAnimation(self, b'size')
        self.animation_pos = QtCore.QPropertyAnimation(self, b'pos')
        self.label = QtWidgets.QLabel('Аля')
    
    def __setting_ui(self) -> None:
        self.setLayout(self.main_v_layout)
        self.main_v_layout.addWidget(self.label)
        self.animation_size.setDuration(500)
        self.animation_pos.setDuration(500)
        self.main_v_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    
    def start_animation(self) -> None:
        self.set_values_for_animation()
        self.animation_size.start()
        self.animation_pos.start()

    def set_values_for_animation(self) -> None:
        self.animation_pos.setStartValue(QtCore.QPoint(10, self.parent.height() - 70) if not self.is_opened \
                                                else QtCore.QPoint(10, 10)) 
        self.animation_pos.setEndValue(QtCore.QPoint(10, 10) if not self.is_opened \
                                                else QtCore.QPoint(10, self.parent.height() - 70))
        
        self.animation_size.setStartValue(QtCore.QSize(self.parent.width() - 20, 0) if not self.is_opened \
                                                        else QtCore.QSize(self.parent.width() - 20, self.parent.height() - 70))
        self.animation_size.setEndValue(QtCore.QSize(self.parent.width() - 20, self.parent.height() - 70) if not self.is_opened \
                                                        else QtCore.QSize(self.parent.width() - 20, 0))

        self.show() if not self.is_opened \
            else self.animation_pos.finished.connect(self.hide_after_finished)
        self.is_opened = not self.is_opened
    
    def hide_after_finished(self) -> None:
        self.animation_pos.finished.disconnect(self.hide_after_finished)
        self.hide()
    
    def size_expand(self) -> None:
        self.resize(self.parent.width() - 20, self.parent.height() - 70)