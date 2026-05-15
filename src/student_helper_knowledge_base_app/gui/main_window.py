from PySide6.QtWidgets import QMainWindow

from src.student_helper_knowledge_base_app.core.services import DataService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.service = DataService()
        self.service.entry_added.connect(self.on_entry_added)
        self.service.section_added.connect(self.on_section_added)
        # ... загрузка начальных данных

    def on_add_entry_clicked(self):
        # Получаем текущий раздел, дату, заголовок, текст из диалога
        new_entry = self.service.create_entry(
            section_id=current_section.id,
            lecture_date=date_selected,
            title=title_edit.text(),
            note=note_edit.toPlainText()
        )
        # Не нужно явно обновлять список – сигнал entry_added вызовет on_entry_added

    def on_entry_added(self, entry):
        self.entries_model.append(entry)   # обновить QTreeView