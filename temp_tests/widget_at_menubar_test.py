import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QWidget, QLabel
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMenuBar с виджетом в углу")

        # 1. Получаем стандартную строку меню
        menubar = self.menuBar()
        menubar.addMenu("Файл")
        menubar.addMenu("Правка")
        menubar.addMenu("Вид")

        # 2. Создаём виджет, который хотим разместить
        search_edit = QLineEdit()
        search_edit.setPlaceholderText("Поиск...")
        search_edit.setFixedWidth(150)

        # 3. Размещаем его в правом верхнем углу
        menubar.setCornerWidget(search_edit, Qt.TopRightCorner)

        self.setCentralWidget(QLabel("Не работает"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec())