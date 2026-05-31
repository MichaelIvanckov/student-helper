import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,
                               QPushButton, QMenu, QLineEdit, QVBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кастомная верхняя панель")

        # Создаём главный виджет, который заменит собой MenuBar
        custom_widget = QWidget()
        layout = QHBoxLayout(custom_widget)
        layout.setContentsMargins(5, 0, 5, 0)

        # --- Имитируем стандартные кнопки меню с помощью QPushButton ---
        btn_file = QPushButton("Файл")
        file_menu = QMenu()
        file_menu.addAction("Открыть")
        file_menu.addAction("Выход", self.close)
        btn_file.setMenu(file_menu)
        layout.addWidget(btn_file)

        btn_edit = QPushButton("Правка")
        edit_menu = QMenu()
        edit_menu.addAction("Копировать")
        btn_edit.setMenu(edit_menu)
        layout.addWidget(btn_edit)

        # --- Добавляем разделитель-растяжку, чтобы отодвинуть другие элементы вправо ---
        layout.addStretch()

        # --- Добавляем строку поиска ---
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Поиск...")
        search_edit.setFixedWidth(150)
        layout.addWidget(search_edit)

        # Устанавливаем наш кастомный виджет в качестве новой строки меню
        self.setMenuWidget(custom_widget)

        # Важно: Не забудьте добавить основной контент в центр окна
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(QPushButton("Пример контента"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 300)
    window.show()
    sys.exit(app.exec())