# main_window.py
import sys
import json
from pathlib import Path
from datetime import date, datetime
from typing import Optional, List, Dict, Any

from PySide6.QtCore import Qt, QDate, QPoint
from PySide6.QtGui import QAction, QIcon, QTextCharFormat
from PySide6.QtWidgets import (
    QMainWindow, QTreeWidgetItem, QMessageBox, QInputDialog, QFileDialog,
    QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QListWidget, QListWidgetItem, QPushButton, QDateEdit,
    QCheckBox, QDialog, QDialogButtonBox, QMenu, QSplitter, QApplication
)
from PySide6.QtCore import Signal

from src.student_helper_knowledge_base_app.core.services import DataService, DataServiceError
from src.student_helper_knowledge_base_app.ui_and_qrc_files.v3.ui_main_window_ui import Ui_MainWindow  # сгенерированный из .ui


# ----------------------------------------------------------------------
# Виджет редактора записи (вкладка)
# ----------------------------------------------------------------------
class EntryEditorWidget(QWidget):
    """Вкладка для просмотра и редактирования одной записи."""
    entry_updated = Signal(int)  # entry_id

    def __init__(self, service: DataService, entry_id: int, parent=None):
        super().__init__(parent)
        self.service = service
        self.entry_id = entry_id
        self.entry = self.service.get_entry_by_id(entry_id)
        if not self.entry:
            raise ValueError(f"Запись {entry_id} не найдена")

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Заголовок и дата
        form_layout = QHBoxLayout()
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Название (опционально)")
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.global_check = QCheckBox("Глобальная запись (без даты)")
        self.global_check.toggled.connect(lambda checked: self.date_edit.setEnabled(not checked))
        self.complete_check = QCheckBox("Запись заполнена")
        form_layout.addWidget(QLabel("Название:"))
        form_layout.addWidget(self.title_edit)
        form_layout.addWidget(QLabel("Дата:"))
        form_layout.addWidget(self.date_edit)
        form_layout.addWidget(self.global_check)
        form_layout.addWidget(self.complete_check)
        layout.addLayout(form_layout)

        # Заметка
        layout.addWidget(QLabel("Заметка:"))
        self.note_edit = QTextEdit()
        layout.addWidget(self.note_edit)

        # Список файлов
        layout.addWidget(QLabel("Прикреплённые файлы:"))
        self.files_list = QListWidget()
        self.files_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.files_list.customContextMenuRequested.connect(self.file_context_menu)
        layout.addWidget(self.files_list)

        # Кнопки управления файлами
        btn_layout = QHBoxLayout()
        self.add_file_btn = QPushButton("Добавить файл")
        self.add_file_btn.clicked.connect(self.add_file)
        self.add_existing_btn = QPushButton("Прикрепить существующий")
        self.add_existing_btn.clicked.connect(self.attach_existing_file)
        self.detach_file_btn = QPushButton("Удалить выбранный")
        self.detach_file_btn.clicked.connect(self.detach_file)
        btn_layout.addWidget(self.add_file_btn)
        btn_layout.addWidget(self.add_existing_btn)
        btn_layout.addWidget(self.detach_file_btn)
        layout.addLayout(btn_layout)

        # Кнопка сохранения
        self.save_btn = QPushButton("Сохранить изменения")
        self.save_btn.clicked.connect(self.save)
        layout.addWidget(self.save_btn)

        # Установим минимальные размеры для планшета
        for btn in [self.add_file_btn, self.add_existing_btn, self.detach_file_btn, self.save_btn]:
            btn.setMinimumHeight(40)

    def load_data(self):
        self.title_edit.setText(self.entry.title or "")
        if self.entry.is_global:
            self.global_check.setChecked(True)
        else:
            self.global_check.setChecked(False)
            if self.entry.lecture_date:
                self.date_edit.setDate(QDate(self.entry.lecture_date.year,
                                             self.entry.lecture_date.month,
                                             self.entry.lecture_date.day))
        self.complete_check.setChecked(self.entry.is_complete)
        self.note_edit.setPlainText(self.entry.note or "")
        self.load_files()

    def load_files(self):
        self.files_list.clear()
        files = self.service.get_files_for_entry(self.entry_id)
        for f in files:
            item = QListWidgetItem(f"{f.original_name} [{f.mime_type}]")
            item.setData(Qt.UserRole, f.id)
            self.files_list.addItem(item)

    def add_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if not path:
            return
        try:
            file_obj = self.service.add_file(path)
            self.service.attach_file_to_entry(self.entry_id, file_obj.id)
            self.load_files()
        except DataServiceError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def attach_existing_file(self):
        # Упрощённо: показать диалог со всеми файлами (или только не привязанными)
        files = self.service.get_all_files()
        if not files:
            QMessageBox.information(self, "Нет файлов", "Нет доступных файлов в хранилище.")
            return
        # простой диалог выбора из списка
        dlg = QDialog(self)
        dlg.setWindowTitle("Выберите файл")
        layout = QVBoxLayout(dlg)
        list_widget = QListWidget()
        for f in files:
            item = QListWidgetItem(f"{f.original_name} ({f.mime_type})")
            item.setData(Qt.UserRole, f.id)
            list_widget.addItem(item)
        layout.addWidget(list_widget)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)
        if dlg.exec() == QDialog.Accepted:
            selected = list_widget.currentItem()
            if selected:
                file_id = selected.data(Qt.UserRole)
                try:
                    self.service.attach_file_to_entry(self.entry_id, file_id)
                    self.load_files()
                except DataServiceError as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

    def detach_file(self):
        current = self.files_list.currentItem()
        if not current:
            return
        file_id = current.data(Qt.UserRole)
        reply = QMessageBox.question(self, "Отвязать файл",
                                     "Отвязать файл от этой записи? (физически не удаляется)",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.service.detach_file(self.entry_id, file_id)
                self.load_files()
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def save(self):
        try:
            is_global = self.global_check.isChecked()
            lecture_date = None if is_global else self.date_edit.date().toPython()
            self.service.update_entry(
                self.entry_id,
                title=self.title_edit.text() or None,
                lecture_date=lecture_date,
                is_global=is_global,
                note=self.note_edit.toPlainText() or None,
                is_complete=self.complete_check.isChecked()
            )
            QMessageBox.information(self, "Сохранено", "Изменения сохранены.")
            self.entry_updated.emit(self.entry_id)
        except DataServiceError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def file_context_menu(self, pos: QPoint):
        item = self.files_list.itemAt(pos)
        if not item:
            return
        menu = QMenu()
        open_action = menu.addAction("Открыть")
        detach_action = menu.addAction("Отвязать")
        action = menu.exec(self.files_list.mapToGlobal(pos))
        file_id = item.data(Qt.UserRole)
        if action == open_action:
            path = self.service.get_file_path(file_id)
            if path and path.exists():
                from PySide6.QtGui import QDesktopServices
                QDesktopServices.openUrl(path.as_uri())
            else:
                QMessageBox.warning(self, "Ошибка", "Файл не найден.")
        elif action == detach_action:
            try:
                self.service.detach_file(self.entry_id, file_id)
                self.load_files()
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))


# ----------------------------------------------------------------------
# Главное окно
# ----------------------------------------------------------------------
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, project_path: Optional[Path] = None):
        super().__init__()
        self.setupUi(self)
        self.service = None
        self.current_section_id = None

        # Настройка элементов
        self.main_tabs.setTabsClosable(True)
        self.main_tabs.tabCloseRequested.connect(self.close_tab)
        self.sections_tree.itemClicked.connect(self.on_tree_item_clicked)
        self.sections_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sections_tree.customContextMenuRequested.connect(self.tree_context_menu)

        # Кнопки действий
        self.create_section_button.clicked.connect(self.add_section)
        self.create_entry_button.clicked.connect(self.add_entry)
        self.load_photo_by_exif_button.clicked.connect(self.add_photos_batch)
        self.search_button.clicked.connect(self.search_notes)

        # Календарь
        self.calendar.clicked.connect(self.on_calendar_day_clicked)

        # Инициализируем сервис и загружаем данные
        self.init_service(project_path)

    def init_service(self, project_path: Optional[Path] = None):
        if project_path and project_path.exists():
            # Загружаем проект (упрощённо: из JSON)
            with open(project_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            db_path = project_path.parent / config['database_path']
            storage_path = project_path.parent / config['storage_path']
            self.service = DataService(db_path=f"sqlite:///{db_path.as_posix()}", storage_dir=storage_path)
            self.setWindowTitle(f"База знаний - {config['name']}")
        else:
            # Создаём новый проект или используем временный (для демо)
            from PySide6.QtCore import QStandardPaths
            default_dir = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)) / "KnowledgeBase"
            default_dir.mkdir(parents=True, exist_ok=True)
            db_path = default_dir / "demo.db"
            storage_path = default_dir / "storage"
            self.service = DataService(db_path=f"sqlite:///{db_path.as_posix()}", storage_dir=storage_path)

        # Подключаем сигналы сервиса
        self.service.section_added.connect(self.on_section_added)
        self.service.section_deleted.connect(self.on_section_deleted)
        self.service.entry_added.connect(self.on_entry_added)
        self.service.entry_deleted.connect(self.on_entry_deleted)
        self.service.entry_updated.connect(self.on_entry_updated)

        self.load_sections()

    def load_sections(self):
        self.sections_tree.clear()
        root_sections = self.service.get_sections(parent_id=None)
        for sect in root_sections:
            self.add_section_item(sect)

    def add_section_item(self, section, parent_item=None):
        item = QTreeWidgetItem(parent_item if parent_item else self.sections_tree)
        item.setText(0, section.name)
        item.setData(0, Qt.UserRole, ("section", section.id))
        # Записи
        entries = self.service.get_entries_by_section(section.id)
        for entry in entries:
            self.add_entry_item(entry, item)
        # Дочерние разделы
        children = self.service.get_sections(parent_id=section.id)
        for child in children:
            self.add_section_item(child, item)
        if parent_item is None:
            self.sections_tree.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        item.setExpanded(True)

    def add_entry_item(self, entry, parent_item):
        item = QTreeWidgetItem(parent_item)
        display = entry.title if entry.title else (entry.lecture_date.isoformat() if entry.lecture_date else "Без даты")
        item.setText(0, display)
        item.setData(0, Qt.UserRole, ("entry", entry.id))
        if entry.is_complete:
            item.setForeground(0, Qt.darkGreen)
        return item

    def on_tree_item_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        kind, obj_id = data
        if kind == "section":
            self.current_section_id = obj_id
            # Обновляем календарь для этого раздела
            self.highlight_calendar_dates(obj_id)
        elif kind == "entry":
            self.open_entry_in_tab(obj_id)

    def open_entry_in_tab(self, entry_id):
        # Проверяем, не открыта ли уже вкладка с этой записью
        for i in range(self.main_tabs.count()):
            widget = self.main_tabs.widget(i)
            if isinstance(widget, EntryEditorWidget) and widget.entry_id == entry_id:
                self.main_tabs.setCurrentIndex(i)
                return
        # Создаём новую вкладку
        editor = EntryEditorWidget(self.service, entry_id)
        editor.entry_updated.connect(lambda eid: self.on_entry_updated(eid))
        # Заголовок вкладки – название записи или дата
        entry = self.service.get_entry_by_id(entry_id)
        tab_title = entry.title if entry.title else (entry.lecture_date.isoformat() if entry.lecture_date else "Без названия")
        self.main_tabs.addTab(editor, tab_title)
        self.main_tabs.setCurrentWidget(editor)

    def close_tab(self, index):
        widget = self.main_tabs.widget(index)
        if isinstance(widget, EntryEditorWidget):
            # Можно спросить о сохранении, но у нас есть кнопка Сохранить
            pass
        self.main_tabs.removeTab(index)
        widget.deleteLater()

    def highlight_calendar_dates(self, section_id):
        # Получаем даты записей в разделе
        entries = self.service.get_entries_by_section(section_id)
        dates = [e.lecture_date for e in entries if e.lecture_date and not e.is_global]
        # Сброс форматирования
        fmt = self.calendar.dateTextFormat()
        for qdate in fmt.keys():
            self.calendar.setDateTextFormat(qdate, fmt[qdate])  # сброс? проще пересоздать
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())  # очистка
        # Подсветка
        for d in dates:
            qd = QDate(d.year, d.month, d.day)
            format = self.calendar.dateTextFormat(qd)
            format.setBackground(Qt.yellow)
            self.calendar.setDateTextFormat(qd, format)

    def on_calendar_day_clicked(self, qdate: QDate):
        if not self.current_section_id:
            QMessageBox.warning(self, "Нет раздела", "Выберите раздел в дереве.")
            return
        selected_date = qdate.toPython()
        entries = self.service.get_entries_by_section(self.current_section_id)
        day_entries = [e for e in entries if e.lecture_date == selected_date and not e.is_global]
        if not day_entries:
            # Создать запись за этот день?
            reply = QMessageBox.question(self, "Нет записи", "Создать запись за этот день?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                entry = self.service.create_entry(
                    section_id=self.current_section_id,
                    lecture_date=selected_date,
                    is_global=False,
                    title=None,
                    note=""
                )
                self.open_entry_in_tab(entry.id)
        else:
            # Открыть первую запись (можно показывать список)
            self.open_entry_in_tab(day_entries[0].id)

    # ---------- Обработчики сигналов сервиса ----------
    def on_section_added(self, section):
        self.load_sections()

    def on_section_deleted(self, section_id):
        self.load_sections()
        if self.current_section_id == section_id:
            self.current_section_id = None

    def on_entry_added(self, entry):
        self.load_sections()
        # Если это текущий раздел, можно переоткрыть, но дерево обновится

    def on_entry_deleted(self, entry_id):
        self.load_sections()
        # Закрыть вкладку, если открыта
        for i in range(self.main_tabs.count()):
            widget = self.main_tabs.widget(i)
            if isinstance(widget, EntryEditorWidget) and widget.entry_id == entry_id:
                self.main_tabs.removeTab(i)
                break

    def on_entry_updated(self, entry_id):
        self.load_sections()
        # Обновить заголовок вкладки, если открыта
        entry = self.service.get_entry_by_id(entry_id)
        if entry:
            tab_title = entry.title if entry.title else (entry.lecture_date.isoformat() if entry.lecture_date else "Без названия")
            for i in range(self.main_tabs.count()):
                widget = self.main_tabs.widget(i)
                if isinstance(widget, EntryEditorWidget) and widget.entry_id == entry_id:
                    self.main_tabs.setTabText(i, tab_title)
                    break

    # ---------- Действия с деревом ----------
    def add_section(self):
        name, ok = QInputDialog.getText(self, "Новый раздел", "Название:")
        if ok and name.strip():
            try:
                parent_id = self.current_section_id if self.current_section_id else None
                self.service.create_section(name.strip(), parent_id)
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def add_entry(self):
        if not self.current_section_id:
            QMessageBox.warning(self, "Нет раздела", "Сначала выберите раздел в дереве.")
            return
        # Простой диалог для MVP
        dialog = QDialog(self)
        dialog.setWindowTitle("Новая запись")
        layout = QVBoxLayout(dialog)
        title_edit = QLineEdit()
        title_edit.setPlaceholderText("Название (опционально)")
        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        global_cb = QCheckBox("Глобальная запись (без даты)")
        note_edit = QTextEdit()
        note_edit.setPlaceholderText("Текст заметки")
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(title_edit)
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(date_edit)
        layout.addWidget(global_cb)
        layout.addWidget(QLabel("Заметка:"))
        layout.addWidget(note_edit)
        layout.addWidget(buttons)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        def toggle_date(checked):
            date_edit.setEnabled(not checked)
        global_cb.toggled.connect(toggle_date)

        if dialog.exec() == QDialog.Accepted:
            lecture_date = None if global_cb.isChecked() else date_edit.date().toPython()
            try:
                self.service.create_entry(
                    section_id=self.current_section_id,
                    lecture_date=lecture_date,
                    is_global=global_cb.isChecked(),
                    title=title_edit.text() or None,
                    note=note_edit.toPlainText() or None
                )
            except DataServiceError as e:
                QMessageBox.critical(self, "Ошибка", str(e))

    def add_photos_batch(self):
        if not self.current_section_id:
            QMessageBox.warning(self, "Нет раздела", "Сначала выберите раздел.")
            return
        paths, _ = QFileDialog.getOpenFileNames(self, "Выберите фото", "", "Images (*.jpg *.jpeg *.png)")
        if not paths:
            return
        # Вызов пакетного метода сервиса
        try:
            result = self.service.add_photos_batch_to_section(paths, self.current_section_id)
            # Обработка успешных
            for entry_id, file_id, photo_date in result['added']:
                QMessageBox.information(self, "Успех", f"Фото от {photo_date} добавлено в запись {entry_id}")
            # Обработка неудачных
            if result['failed']:
                self.handle_failed_photos(result['failed'], self.current_section_id)
        except DataServiceError as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def handle_failed_photos(self, failed_list, section_id):
        for file_path, error in failed_list:
            dlg = QDialog(self)
            dlg.setWindowTitle("Неизвестная дата фото")
            layout = QVBoxLayout(dlg)
            layout.addWidget(QLabel(f"Файл: {Path(file_path).name}\n{error}"))
            date_edit = QDateEdit()
            date_edit.setDate(QDate.currentDate())
            layout.addWidget(QLabel("Выберите дату лекции:"))
            layout.addWidget(date_edit)
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dlg.accept)
            buttons.rejected.connect(dlg.reject)
            layout.addWidget(buttons)
            if dlg.exec() == QDialog.Accepted:
                chosen_date = date_edit.date().toPython()
                try:
                    entry = self.service.ensure_entry_by_date(section_id, chosen_date)
                    self.service.add_photo_to_entry_by_file(file_path, entry.id)
                    QMessageBox.information(self, "Готово", f"Фото добавлено в запись от {chosen_date}")
                except DataServiceError as e:
                    QMessageBox.critical(self, "Ошибка", str(e))

    def search_notes(self):
        keyword = self.search_line_edit.text().strip()
        if not keyword:
            return
        results = self.service.search_notes(keyword)
        # Создаём вкладку с результатами
        tab = QWidget()
        layout = QVBoxLayout(tab)
        list_widget = QListWidget()
        for entry in results:
            display = entry.title if entry.title else (entry.lecture_date.isoformat() if entry.lecture_date else "Без даты")
            item = QListWidgetItem(f"{display} (раздел {entry.section_id})")
            item.setData(Qt.UserRole, entry.id)
            list_widget.addItem(item)
        list_widget.itemDoubleClicked.connect(lambda item: self.open_entry_in_tab(item.data(Qt.UserRole)))
        layout.addWidget(list_widget)
        self.main_tabs.addTab(tab, f"Поиск: {keyword}")
        self.main_tabs.setCurrentWidget(tab)

    def tree_context_menu(self, pos: QPoint):
        item = self.sections_tree.itemAt(pos)
        if not item:
            return
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        kind, obj_id = data
        menu = QMenu()
        if kind == "section":
            add_entry_act = menu.addAction("Создать запись")
            add_section_act = menu.addAction("Создать подраздел")
            rename_act = menu.addAction("Переименовать")
            delete_act = menu.addAction("Удалить раздел")
            action = menu.exec(self.sections_tree.mapToGlobal(pos))
            if action == add_entry_act:
                self.current_section_id = obj_id
                self.add_entry()
            elif action == add_section_act:
                name, ok = QInputDialog.getText(self, "Новый подраздел", "Название:")
                if ok and name.strip():
                    self.service.create_section(name.strip(), obj_id)
            elif action == rename_act:
                new_name, ok = QInputDialog.getText(self, "Переименовать", "Новое название:", text=item.text(0))
                if ok and new_name.strip():
                    self.service.update_section(obj_id, name=new_name.strip())
            elif action == delete_act:
                reply = QMessageBox.question(self, "Удаление", "Удалить раздел и все его записи?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.service.delete_section(obj_id)
        elif kind == "entry":
            rename_act = menu.addAction("Переименовать")
            delete_act = menu.addAction("Удалить запись")
            action = menu.exec(self.sections_tree.mapToGlobal(pos))
            if action == rename_act:
                new_title, ok = QInputDialog.getText(self, "Переименовать запись", "Новое название:", text=item.text(0))
                if ok:
                    self.service.update_entry(obj_id, title=new_title.strip() or None)
            elif action == delete_act:
                reply = QMessageBox.question(self, "Удаление", "Удалить запись?",
                                             QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.service.delete_entry(obj_id)