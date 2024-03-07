from PySide6 import QtWidgets, QtCore, QtGui


class AnimatedPanel(QtWidgets.QFrame):
    is_opened: bool = False
    main_v_layout: QtWidgets.QVBoxLayout = None
    animation_pos: QtCore.QPropertyAnimation = None
    animation_size: QtCore.QPropertyAnimation = None
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(AnimatedPanel, self).__init__(parent)
        self.parent: QtWidgets.QMainWindow = parent
        self.__init_ui()
        self.__setting_ui()
        self.hide()
    
    def __init_ui(self) -> None:
        self.main_v_layout = QtWidgets.QHBoxLayout()
        self.animation_size = QtCore.QPropertyAnimation(self, b'size')
        self.animation_pos = QtCore.QPropertyAnimation(self, b'pos')
        self.animation_size.setTargetObject(self)
        self.animation_pos.setTargetObject(self)
    
    def __setting_ui(self) -> None:
        self.animation_size.setDuration(500)
        self.animation_pos.setDuration(500)
        
    def start_animation(self, 
                        start_value_pos: QtCore.QPoint = None, 
                        end_value_pos: QtCore.QPoint = None,
                        start_value_size: QtCore.QPoint = None,
                        end_value_size: QtCore.QPoint = None) -> None:
        self.set_values_for_animation(start_value_pos if start_value_pos else QtCore.QPoint(10, self.parent.height() - 70),
                                      end_value_pos if end_value_pos else QtCore.QPoint(10, 10),
                                      start_value_size if start_value_size else QtCore.QSize(self.parent.width() - 20, 0),
                                      end_value_size if end_value_size else QtCore.QSize(self.parent.width() - 20, self.parent.height() - 70))
        self.animation_size.start()
        self.animation_pos.start()

    def set_values_for_animation(self, 
                                 start_value_pos: QtCore.QPoint, 
                                 end_value_pos: QtCore.QPoint,
                                 start_value_size: QtCore.QPoint,
                                 end_value_size: QtCore.QPoint
                                 ) -> None:
        self.animation_pos.setStartValue(start_value_pos if not self.is_opened \
                                                else end_value_pos) 
        self.animation_pos.setEndValue(end_value_pos if not self.is_opened \
                                                else start_value_pos)
        
        self.animation_size.setStartValue(start_value_size if not self.is_opened \
                                                        else end_value_size)
        self.animation_size.setEndValue(end_value_size if not self.is_opened \
                                                        else start_value_size)

        self.show() if not self.is_opened \
            else self.animation_pos.finished.connect(self.hide_after_finished)
        
        self.is_opened = not self.is_opened
    
    def hide_after_finished(self) -> None:
        self.animation_pos.finished.disconnect(self.hide_after_finished)
        self.hide()
    
    def size_expand(self) -> None:
        self.resize(self.parent.width() - 20, self.parent.height() - 70)