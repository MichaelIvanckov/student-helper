import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QWidget,
                               QHBoxLayout, QPushButton, QVBoxLayout, QLabel)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction

class CustomTitleBar(QWidget):
    """Собственная строка заголовка с меню и кнопками"""
    def __init__(self, parent, menubar):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(35)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        # Встраиваем существующую строку меню (QMenuBar)
        layout.addWidget(menubar, 1)  # растягиваем меню

        # Кнопки управления окном
        self.min_btn = QPushButton("—")
        self.max_btn = QPushButton("□")
        self.close_btn = QPushButton("✕")
        for btn in (self.min_btn, self.max_btn, self.close_btn):
            btn.setFixedSize(30, 25)
            layout.addWidget(btn)

        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.max_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.parent.close)

        # Для перетаскивания окна
        self.drag_pos = None

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos is not None:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.parent.move(self.parent.pos() + delta)
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Убираем стандартную рамку
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Меню в заголовке")

        # Создаём строку меню
        menubar = QMenuBar(self)  # не используем self.menuBar()
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Открыть")
        file_menu.addAction("Выход", self.close)

        view_menu = menubar.addMenu("Вид")
        view_menu.addAction("Тёмная тема")

        # Создаём собственную строку заголовка
        title_bar = CustomTitleBar(self, menubar)

        # Основной контент
        central = QLabel("Содержимое окна", alignment=Qt.AlignCenter)
        central.setStyleSheet("background-color: #f0f0f0;")

        # Компоновка: заголовок + центральный виджет
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        main_layout.addWidget(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())