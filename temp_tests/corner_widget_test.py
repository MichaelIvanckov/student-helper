import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget,
    QTextEdit, QPushButton, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример setCornerWidget")
        self.resize(600, 400)

        # Создаем виджет с вкладками
        self.tabs = QTabWidget()

        # Добавляем несколько вкладок для примера
        self.tabs.addTab(QTextEdit(), "Вкладка 1")
        self.tabs.addTab(QTextEdit(), "Вкладка 2")

        # --- 1. КНОПКА НА ВКЛАДКАХ ---
        # Создаем кнопку "+" для добавления новых вкладок
        add_tab_btn = QPushButton("➕")
        add_tab_btn.clicked.connect(self.add_new_tab)
        # Устанавливаем ее в правом верхнем углу (Qt.TopRightCorner по умолчанию)
        self.tabs.setCornerWidget(add_tab_btn, Qt.TopRightCorner)

        # --- 2. КНОПКА В УГЛУ ПРОКРУТКИ ---
        # Создаем область прокрутки (QTextEdit сам наследует QAbstractScrollArea)
        text_edit = QTextEdit()
        text_edit.setPlainText("Это текстовое поле с прокруткой...")

        # Создаем кнопку для угла прокрутки
        info_btn = QPushButton("ℹ️")
        info_btn.setFixedSize(20, 20) # Устанавливаем фиксированный размер для красоты
        info_btn.clicked.connect(lambda: print("Информация"))
        # Устанавливаем кнопку в угол (пересечение полос прокрутки)
        # Чтобы угол был виден, убедимся, что полосы прокрутки всегда включены
        text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        text_edit.setCornerWidget(info_btn)

        # Делаем QTextEdit еще одной вкладкой
        self.tabs.addTab(text_edit, "С угловой кнопкой")

        # Устанавливаем виджет с вкладками как центральный виджет окна
        self.setCentralWidget(self.tabs)

    def add_new_tab(self):
        """Функция для добавления новой вкладки."""
        new_tab = QTextEdit()
        new_tab.setPlainText("Новая вкладка")
        count = self.tabs.count()
        self.tabs.addTab(new_tab, f"Вкладка {count + 1}")

# Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())