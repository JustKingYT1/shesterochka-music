from PySide6.QtWidgets import QWidget
from settings import STYLE_DIR

def set_style_sheet_for_widget(widget: QWidget, file_name: str) -> None:
    with open(f'{STYLE_DIR}/{file_name}', 'r') as file:
        widget.setStyleSheet(file.read())