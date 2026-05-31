#!/usr/bin/env python3
"""
Точка входа для тестирования MainWindow
"""

import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь, чтобы импортировать модули
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication, QMainWindow
from ui_main_window_ui import Ui_MainWindow


USE_MATERIAL_DESIGN = 0

if USE_MATERIAL_DESIGN:
    from qt_material import apply_stylesheet


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)

    if USE_MATERIAL_DESIGN:
        apply_stylesheet(app, theme='dark_teal.xml')

    # Создаём папку для данных, если её нет
    Path("data/storage").mkdir(parents=True, exist_ok=True)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()