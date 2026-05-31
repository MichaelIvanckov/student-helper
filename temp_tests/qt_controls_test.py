import sys
import io
import contextlib

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QPushButton, QLabel, QTextEdit,
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog, QLineEdit,
    QGroupBox, QFormLayout, QDateEdit, QCheckBox, QDialog, QDialogButtonBox, QApplication
)
from PySide6.QtCore import Qt, QDate
# from PySide6.QGuiApplication import QDesktopServices
from PySide6.QtGui import QDesktopServices


class Service:
    def __init__(self):
        self.globals = globals().copy()
        self.locals = locals().copy()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.service = Service()
        self.centralwidget = QWidget(self)
        self.layout = QFormLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.buttonEval = QPushButton("Eval")
        self.buttonExec = QPushButton("Exec")
        self.textEdit = QTextEdit()
        self.lineEdit = QLineEdit()
        self.lineOutput = QLineEdit()
        self.lineOutput.setReadOnly(True)
        self.stderr_label = QLabel("stderr:")
        self.errorOutput = QTextEdit()
        self.errorOutput.setReadOnly(True)
        self.stdout_label = QLabel("stdout:")
        self.stdoutOutput = QTextEdit()
        self.stdoutOutput.setReadOnly(True)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.buttonEval)
        self.layout.addWidget(self.lineOutput)
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.buttonExec)
        self.layout.addWidget(self.stdout_label)
        self.layout.addWidget(self.stdoutOutput)
        self.layout.addWidget(self.stderr_label)
        self.layout.addWidget(self.errorOutput)
        self.buttonEval.clicked.connect(self._eval)
        self.buttonExec.clicked.connect(self._exec)

    def _eval(self):
        line = str(self.lineEdit.text())
        f = io.StringIO()
        err = io.StringIO()
        try:
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(err):
                result = eval(line, self.service.globals, self.service.locals)
            self.lineOutput.setText(repr(result))
            self.errorOutput.append(err.getvalue().strip())
            self.stdoutOutput.append(f.getvalue().strip())
        except Exception as e:
            self.errorOutput.append(str(e))

    def _exec(self):
        text = self.textEdit.toPlainText()
        f = io.StringIO()
        err = io.StringIO()
        try:
            with contextlib.redirect_stdout(f), contextlib.redirect_stderr(err):
                exec(text, self.service.globals, self.service.locals)
            self.errorOutput.append(err.getvalue().strip())
            self.stdoutOutput.append(f.getvalue().strip())
        except Exception as e:
            self.errorOutput.append(str(e))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()