import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTabWidget,
                             QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QMessageBox)
from PySide6.QtCore import Qt


class BrowserTabs(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Включаем возможность закрывать вкладки
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        # Создаём кнопку «+» и помещаем её в правый угол панели вкладок
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(30, 25)  # небольшой размер
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.setCornerWidget(self.add_tab_button, Qt.Corner.TopRightCorner)

        # Добавляем первую вкладку
        self.add_new_tab()

    def add_new_tab(self):
        """Создаёт новую вкладку с текстовым полем"""
        index = self.count() + 1
        tab = QWidget()
        layout = QVBoxLayout(tab)
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(f"Содержимое вкладки {index}")
        layout.addWidget(text_edit)

        self.addTab(tab, f"Вкладка {index}")
        self.setCurrentIndex(self.count() - 1)

    def close_tab(self, index):
        """Закрывает вкладку, не давая удалить последнюю"""
        if self.count() > 1:
            widget = self.widget(index)
            self.removeTab(index)
            widget.deleteLater()
        else:
            QMessageBox.warning(self, "Предупреждение",
                                "Нельзя закрыть последнюю вкладку")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вкладки как в браузере")
        self.setGeometry(100, 100, 900, 600)

        tabs = BrowserTabs()
        self.setCentralWidget(tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())