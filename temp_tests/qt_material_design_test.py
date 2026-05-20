import sys
from PySide6 import QtWidgets
from qt_material import apply_stylesheet

app = QtWidgets.QApplication(sys.argv)

# Создаем главное окно
window = QtWidgets.QMainWindow()
window.setWindowTitle("Модное приложение")
window.resize(600, 400)

# Применяем стиль Material Design (темный бирюзовый)
apply_stylesheet(app, theme='dark_teal.xml')

window.show()
sys.exit(app.exec())