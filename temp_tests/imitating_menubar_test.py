import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QToolBar, QToolButton,
                               QMenu, QLineEdit)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Гибкое меню с помощью QToolBar")

        # Создаём панель инструментов и делаем её похожей на строку меню
        toolbar = QToolBar("Главное меню")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # 1. Создаём пункт меню "Файл"
        btn_file = QToolButton()
        btn_file.setText("Файл")
        btn_file.setPopupMode(QToolButton.InstantPopup)  # Меню открывается сразу
        file_menu = QMenu()
        file_menu.addAction("Открыть")
        file_menu.addAction("Сохранить")
        btn_file.setMenu(file_menu)
        toolbar.addWidget(btn_file)

        # 2. Создаём пункт меню "Правка"
        btn_edit = QToolButton()
        btn_edit.setText("Правка")
        btn_edit.setPopupMode(QToolButton.InstantPopup)
        edit_menu = QMenu()
        edit_menu.addAction("Копировать")
        edit_menu.addAction("Вставить")
        btn_edit.setMenu(edit_menu)
        toolbar.addWidget(btn_edit)

        # 3. Добавляем разделитель
        toolbar.addSeparator()

        # 4. Добавляем произвольный виджет — строку поиска
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Быстрый поиск...")
        toolbar.addWidget(search_edit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec())