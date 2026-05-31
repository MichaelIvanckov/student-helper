import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QWidgetAction,
                               QSlider, QLabel, QHBoxLayout, QWidget)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пример меню с виджетами")

        # Создаём строку меню
        menubar = self.menuBar()

        # Меню "Файл"
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction("Открыть", self.open_file)
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.close)

        # Меню "Вид"
        view_menu = menubar.addMenu("Вид")

        # Обычное действие
        view_menu.addAction("Обычный пункт")

        # Добавляем слайдер (виджет) в меню
        slider_action = QWidgetAction(view_menu)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        slider_action.setDefaultWidget(slider)
        view_menu.addAction(slider_action)

        # Добавляем произвольный составной виджет
        custom_action = QWidgetAction(view_menu)
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(QLabel("Громкость:"))
        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setFixedWidth(100)
        layout.addWidget(volume_slider)
        custom_action.setDefaultWidget(container)
        view_menu.addAction(custom_action)

    def open_file(self):
        print("Открытие файла...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())