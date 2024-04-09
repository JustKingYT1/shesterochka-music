from PySide6 import QtWidgets, QtCore, QtGui
from src.client.music_session import MusicSession
from src.client.tools.style_setter import set_style_sheet_for_widget


class TimerDialog(QtWidgets.QDialog):
    min: int = 0
    secs: int = 0
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.Popup)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)  
        self.__init_ui()
        self.__setting_ui()
    
    def __init_ui(self) -> None:
        self.main_h_layout = QtWidgets.QHBoxLayout()
        self.timer_widget = QtWidgets.QTimeEdit()
        self.timer = QtCore.QTimer(self)
    
    def __setting_ui(self) -> None:
        self.setLayout(self.main_h_layout)
        self.setObjectName('TimerDialog')

        set_style_sheet_for_widget(self, 'timer_dialog.qss')

        self.timer_widget.setDisplayFormat('mm:ss')

        self.main_h_layout.addWidget(self.timer_widget)

        self.timer.timeout.connect(self.update_timer)

        self.adjustSize()
    
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Return.numerator:
            self.start_timer()

    def start_timer(self) -> None:
        time = self.timer_widget.time().toString()
        time_codes = time.split(':')

        time_codes.pop(0)

        self.min = int(time_codes[0])
        self.secs = int(time_codes[1])

        vremya = self.min * 60 + self.secs

        self.parent.timer_button.toggle_pressed()
        
        self.timer.start(900)

        self.parent.music_session.start_stop_timer(vremya)

    def move_to_new_pos(self, pos: QtCore.QPoint) -> None:
        self.move(pos)

    def update_timer(self) -> None:
        if self.parent.music_session.playbackState() == MusicSession.PlaybackState.PlayingState: 
            self.timer_widget.setEnabled(True)
            self.timer_widget.setTime(QtCore.QTime(0, self.min, self.secs, 0))
            if self.min >= 0:
                self.secs -= 1
                if self.secs < 0:
                    self.secs = 60
                    self.min -= 1
        else:
            self.timer_widget.setEnabled(False)
            self.timer_widget.setTime(QtCore.QTime(0, 0, 0, 0))


