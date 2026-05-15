import sys
from pathlib import Path
from datetime import date

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QPushButton, QLabel, QTextEdit,
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog, QLineEdit,
    QGroupBox, QFormLayout, QDateEdit, QCheckBox, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QGuiApplication import QDesktopServices

from data_service import DataService, DataServiceError


class CreateEntryDialog(QDialog):
    """Диалог создания новой записи."""
    def __init__(self, section_id, parent=None):
        super().__init__(parent)
        self.section_id = section_id
        self.setWindowTitle("Новая запись")
        layout = QFormLayout(self)

        self.title_edit = QLineEdit()
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.global_cb = QCheckBox("Глобальная (не привязана к дате)")
        self.global_cb.toggled.connect(self.on_global_toggled)
        self.note_edit = QTextEdit()
        self.note_edit.setMaximumHeight(100)

        layout.addRow("Название (опционально):", self.title_edit)
        layout.addRow("Дата лекции:", self.date_edit)
        layout.addRow(self.global_cb)
        layout.addRow("Текст заметки:", self.note_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def on_global_toggled(self, checked):
        self.date_edit.setEnabled(not checked)

    def get_data(self):
        lecture_date = None if self.global_cb.isChecked() else self.date_edit.date().toPython()
        return {
            "section_id": self.section_id,
            "lecture_date": lecture_date,
            "is_global": self.global_cb.isChecked(),
            "title": self.title_edit.text() or None,
            "note": self.note_edit.toPlainText() or None
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("База знаний студента — тестовый прототип")
        self.resize(1000, 700)

        # Инициализация сервиса
        try:
            self.service = DataService()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось инициализировать БД: {e}")
            sys.exit(1)

        # Подключаем сигналы сервиса к слотам обновления GUI
        self.service.section_added.connect(self.on_section_added)
        self.service.section_deleted.connect(self.on_section_deleted)
        self.service.entry_added.connect(self.on_entry_added)
        self.service.entry_deleted.connect(self.on_entry_deleted)
        self.service.entry_updated.connect(self.on_entry_updated)
        self.service.file_attached.connect(self.on_file_attached)
        self.service.file_detached.connect(self.on_file_detached)

        self.setup_ui()

        # Загружаем начальные данные
        self.load_sections()

    def setup_ui(self):
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Левая панель: дерево разделов и записей
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Разделы и записи")
        self.tree.itemClicked.connect(self.on_tree_item_clicked)
        left_layout.addWidget(self.tree)

        # Кнопки управления разделами/записями
        btn_layout = QHBoxLayout()
        self.btn_add_section = QPushButton("+ Раздел")
        self.btn_add_section.clicked.connect(self.add_section)
        self.btn_add_entry = QPushButton("+ Запись")
        self.btn_add_entry.clicked.connect(self.add_entry)
        self.btn_delete = QPushButton("Удалить")
        self.btn_delete.clicked.connect(self.delete_current_item)
        btn_layout.addWidget(self.btn_add_section)
        btn_layout.addWidget(self.btn_add_entry)
        btn_layout.addWidget(self.btn_delete)
        left_layout.addLayout(btn_layout)

        # Правая панель: детали записи и файлы
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        # Область информации о записи
        self.entry_info = QGroupBox("Информация о записи")
        info_layout = QVBoxLayout()
        self.entry_title_label = QLabel("Название: —")
        self.entry_date_label = QLabel("Дата: —")
        self.entry_note_label = QLabel("Заметка: ")
        self.entry_note_text = QTextEdit()
        self.entry_note_text.setReadOnly(True)
        self.entry_note_text.setMaximumHeight(80)
        info_layout.addWidget(self.entry_title_label)
        info_layout.addWidget(self.entry_date_label)
        info_layout.addWidget(self.entry_note_label)
        info_layout.addWidget(self.entry_note_text)
        self.entry_info.setLayout(info_layout)
        right_layout.addWidget(self.entry_info)

        # Список файлов записи
        self.files_list = QListWidget()
        self.files_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.files_list.customContextMenuRequested.connect(self.file_context_menu)
        right_layout.addWidget(QLabel("Прикреплённые файлы:"))
        right_layout.addWidget(self.files_list)

        # Кнопки действий с файлами
        file_btn_layout = QHBoxLayout()
        self.btn_add_file = QPushButton("Добавить файл")
        self.btn_add_file.clicked.connect(self.add_file_to_entry)
        self.btn_add_photo = QPushButton("Добавить фото (по дате)")
        self.btn_add_photo.clicked.connect(self.add_photo_by_metadata)
        file_btn_layout.addWidget(self.btn_add_file)
        file_btn_layout.addWidget(self.btn_add_photo)
        right_layout.addLayout(file_btn_layout)

        # Поиск
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по заметкам...")
        self.btn_search = QPushButton("Найти")
        self.btn_search.clicked.connect(self.search_notes)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.btn_search)
        right_layout.addLayout(search_layout)

        # Размещаем левую и правую панели через сплиттер
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)

        # Переменные для хранения текущего выбранного элемента
        self.current_section_id = None
        self.current_entry_id = None

    # ----------------------------------------------------------------------
    # Загрузка данных
    # ----------------------------------------------------------------------
    def load_sections(self):
        self.tree.clear()
        root_sections = self.service.get_sections(parent_id=None)
        for sect in root_sections:
            self.add_section_to_tree(sect)

    def add_section_to_tree(self, section, parent_item=None):
        item = QTreeWidgetItem(parent_item if parent_item else self.tree)
        item.setText(0, section.name)
        item.setData(0, Qt.UserRole, ("section", section.id))
        # Загружаем записи этого раздела
        entries = self.service.get_entries_by_section(section.id)
        for entry in entries:
            self.add_entry_to_tree(entry, item)
        # Загружаем дочерние разделы
        children = self.service.get_sections(parent_id=section.id)
        for child in children:
            self.add_section_to_tree(child, item)
        if parent_item is None:
            self.tree.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        item.setExpanded(True)

    def add_entry_to_tree(self, entry, parent_item):
        item = QTreeWidgetItem(parent_item)
        display = entry.title if entry.title else (entry.lecture_date.isoformat() if entry.lecture_date else "Без даты")
        item.setText(0, display)
        item.setData(0, Qt.UserRole, ("entry", entry.id))

    # ----------------------------------------------------------------------
    # Обработчики сигналов сервиса
    # ----------------------------------------------------------------------
    def on_section_added(self, section):
        # Добавляем в дерево (упрощённо – перезагружаем всё)
        self.load_sections()

    def on_section_deleted(self, section_id):
        self.load_sections()
        if self.current_section_id == section_id:
            self.clear_entry_display()

    def on_entry_added(self, entry):
        self.load_sections()
        # Если это текущий раздел, можно выделить новую запись
        if self.current_section_id == entry.section_id:
            # Не будем усложнять – просто перезагрузили
            pass

    def on_entry_deleted(self, entry_id):
        if self.current_entry_id == entry_id:
            self.clear_entry_display()
        self.load_sections()

    def on_entry_updated(self, entry):
        if self.current_entry_id == entry.id:
            self.display_entry(entry)
        self.load_sections()  # обновить название в дереве

    def on_file_attached(self, entry_id, file_id):
        if self.current_entry_id == entry_id:
            self.load_files_for_current_entry()

    def on_file_detached(self, entry_id, file_id):
        if self.current_entry_id == entry_id:
            self.load_files_for_current_entry()

    # ----------------------------------------------------------------------
    # Отображение деталей записи
    # ----------------------------------------------------------------------
    def clear_entry_display(self):
        self.current_entry_id = None
        self.entry_title_label.setText("Название: —")
        self.entry_date_label.setText("Дата: —")
        self.entry_note_text.clear()
        self.files_list.clear()
        self.btn_add_file.setEnabled(False)
        self.btn_add_photo.setEnabled(False)

    def display_entry(self, entry):
        self.current_entry_id = entry.id
        title = entry.title if entry.title else "(без названия)"
        self.entry_title_label.setText(f"Название: {title}")
        if entry.is_global:
            date_str = "Глобальная запись"
        else:
            date_str = entry.lecture_date.isoformat() if entry.lecture_date else "Дата не указана"
        self.entry_date_label.setText(f"Дата: {date_str}")
        self.entry_note_text.setPlainText(entry.note if entry.note else "")
        self.load_files_for_current_entry()
        self.btn_add_file.setEnabled(True)
        self.btn_add_photo.setEnabled(True)

    def load_files_for_current_entry(self):
        self.files_list.clear()
        if not self.current_entry_id:
            return
        files = self.service.get_files_for_entry(self.current_entry_id)
        for file_obj in files:
            item = QListWidgetItem(f"{file_obj.original_name} [{file_obj.mime_type}]")
            item.setData(Qt.UserRole, file_obj.id)
            self.files_list.addItem(item)

    # ----------------------------------------------------------------------
    # Обработка кликов в дереве
    # ----------------------------------------------------------------------
    def on_tree_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        kind, obj_id = data
        if kind == "section":
            self.current_section_id = obj_id
            self.current_entry_id = None
            self.clear_entry_display()
        elif kind == "entry":
            entry = self.service.get_entry_by_id(obj_id)
            if entry:
                self.current_section_id = entry.section_id
                self.display_entry(entry)
            else:
                self.clear_entry_display()

    # ----------------------------------------------------------------------
    # Действия: разделы, записи, удаление
    # ----------------------------------------------------------------------
    def add_section(self):
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, "Новый раздел", "Название раздела:")
        if ok and name.strip():
            try:
                self.service.create_section(name.strip())
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def add_entry(self):
        if self.current_section_id is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите раздел в дереве.")
            return
        dialog = CreateEntryDialog(self.current_section_id, self)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.service.create_entry(**data)
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def delete_current_item(self):
        current = self.tree.currentItem()
        if not current:
            return
        data = current.data(0, Qt.UserRole)
        if not data:
            return
        kind, obj_id = data
        if kind == "section":
            reply = QMessageBox.question(self, "Удаление", "Удалить раздел и все его записи?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.service.delete_section(obj_id)
                except DataServiceError as e:
                    QMessageBox.critical(self, "Ошибка", str(e))
        elif kind == "entry":
            reply = QMessageBox.question(self, "Удаление", "Удалить запись?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.service.delete_entry(obj_id)
                except DataServiceError as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

    # ----------------------------------------------------------------------
    # Работа с файлами
    # ----------------------------------------------------------------------
    def add_file_to_entry(self):
        if not self.current_entry_id:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите запись.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if not file_path:
            return
        try:
            # Сначала добавляем файл в хранилище
            file_obj = self.service.add_file(file_path)
            # Привязываем к текущей записи
            self.service.attach_file_to_entry(self.current_entry_id, file_obj.id)
            QMessageBox.information(self, "Готово", "Файл прикреплён.")
        except DataServiceError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def add_photo_by_metadata(self):
        if not self.current_section_id:
            QMessageBox.warning(self, "Предупреждение", "Сначала выберите раздел в дереве.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.jpg *.jpeg *.png *.tiff)")
        if not file_path:
            return
        try:
            entry = self.service.add_photo_by_metadata(self.current_section_id, file_path)
            QMessageBox.information(self, "Готово", f"Фото добавлено в запись от {entry.lecture_date}")
            # После создания новой записи дерево перезагрузится через сигнал
        except DataServiceError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def file_context_menu(self, pos):
        item = self.files_list.itemAt(pos)
        if not item:
            return
        file_id = item.data(Qt.UserRole)
        menu = self.files_list.createStandardContextMenu()
        open_action = menu.addAction("Открыть файл")
        detach_action = menu.addAction("Отвязать от записи")
        action = menu.exec(self.files_list.mapToGlobal(pos))
        if action == open_action:
            self.open_file(file_id)
        elif action == detach_action:
            self.detach_file(file_id)

    def open_file(self, file_id):
        path = self.service.get_file_path(file_id)
        if path and path.exists():
            QDesktopServices.openUrl(path.as_uri())
        else:
            QMessageBox.warning(self, "Ошибка", "Файл не найден на диске.")

    def detach_file(self, file_id):
        if not self.current_entry_id:
            return
        reply = QMessageBox.question(self, "Отвязка", "Отвязать файл от этой записи? (физически не удаляется)",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.service.detach_file(self.current_entry_id, file_id)
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    # ----------------------------------------------------------------------
    # Поиск
    # ----------------------------------------------------------------------
    def search_notes(self):
        keyword = self.search_edit.text().strip()
        if not keyword:
            return
        results = self.service.search_notes(keyword)
        if not results:
            QMessageBox.information(self, "Поиск", "Ничего не найдено.")
            return
        # Покажем в отдельном диалоге
        from PySide6.QtWidgets import QDialog, QListWidget, QVBoxLayout
        dlg = QDialog(self)
        dlg.setWindowTitle("Результаты поиска")
        layout = QVBoxLayout(dlg)
        list_widget = QListWidget()
        for entry in results:
            display = entry.title if entry.title else (entry.lecture_date.isoformat() if entry.lecture_date else "Без даты")
            item = QListWidgetItem(f"{display} (раздел {entry.section_id})")
            item.setData(Qt.UserRole, entry.id)
            list_widget.addItem(item)
        list_widget.itemDoubleClicked.connect(lambda it: self.jump_to_entry(it.data(Qt.UserRole), dlg))
        layout.addWidget(list_widget)
        btn = QPushButton("Закрыть")
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn)
        dlg.resize(400, 300)
        dlg.exec()

    def jump_to_entry(self, entry_id, dialog):
        # Найти запись в дереве и выделить её
        # Упрощённо: перезагрузим дерево и найдём элемент
        # В реальном приложении нужен поиск по дереву. Здесь сделаем простой способ:
        self.load_sections()
        # Поиск в дереве (рекурсивно)
        def find_item(parent_item):
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                data = child.data(0, Qt.UserRole)
                if data and data[0] == "entry" and data[1] == entry_id:
                    return child
                found = find_item(child)
                if found:
                    return found
            return None
        for i in range(self.tree.topLevelItemCount()):
            top = self.tree.topLevelItem(i)
            if top.data(0, Qt.UserRole) and top.data(0, Qt.UserRole)[0] == "entry" and top.data(0, Qt.UserRole)[1] == entry_id:
                self.tree.setCurrentItem(top)
                self.on_tree_item_clicked(top, 0)
                dialog.accept()
                return
            found = find_item(top)
            if found:
                self.tree.setCurrentItem(found)
                self.on_tree_item_clicked(found, 0)
                dialog.accept()
                return
        QMessageBox.warning(self, "Не найдено", "Запись не отображается в текущем дереве.")