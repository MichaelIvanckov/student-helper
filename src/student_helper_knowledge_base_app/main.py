#!/usr/bin/env python3
"""
Точка входа для тестирования DataService.
Запускает главное окно приложения.
"""

import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь, чтобы импортировать модули
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


USE_MATERIAL_DESIGN = False

if USE_MATERIAL_DESIGN:
    from qt_material import apply_stylesheet


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