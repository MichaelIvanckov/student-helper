from PySide6.QtCore import QObject, Signal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Section, Entry, File, FileLink
from datetime import date, datetime
from pathlib import Path
import shutil
import json
from PIL import Image
from PIL.ExifTags import TAGS

class DataService(QObject):
    # Сигналы для уведомления GUI об изменениях
    section_added = Signal(object)   # передаём объект Section
    section_deleted = Signal(int)    # id раздела
    entry_added = Signal(object)     # объект Entry
    entry_updated = Signal(object)
    entry_deleted = Signal(int)
    file_attached = Signal(int, int) # entry_id, file_id
    file_detached = Signal(int, int)
    data_reset = Signal()            # при полной перезагрузке БД

    def __init__(self, db_path='sqlite:///data/app_data.db'):
        super().__init__()
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self._storage_dir = Path('data/storage')
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    # ----- Управление сессией (контекстный менеджер) -----
    def _get_session(self):
        return self.Session()

    # ----- Разделы -----
    def create_section(self, name, parent_id=None):
        with self._get_session() as session:
            section = Section(name=name, parent_section_id=parent_id)
            session.add(section)
            session.commit()
            self.section_added.emit(section)
            return section

    def delete_section(self, section_id):
        with self._get_session() as session:
            section = session.query(Section).get(section_id)
            if section:
                session.delete(section)
                session.commit()
                self.section_deleted.emit(section_id)

    def get_sections(self, parent_id=None):
        with self._get_session() as session:
            q = session.query(Section)
            if parent_id is None:
                q = q.filter(Section.parent_section_id.is_(None))
            else:
                q = q.filter(Section.parent_section_id == parent_id)
            return q.all()

    # ----- Записи -----
    def create_entry(self, section_id, lecture_date=None, is_global=False, title=None, note=None):
        with self._get_session() as session:
            entry = Entry(
                section_id=section_id,
                lecture_date=lecture_date,
                is_global=is_global,
                title=title,
                note=note
            )
            session.add(entry)
            session.commit()
            self.entry_added.emit(entry)
            return entry

    def update_entry(self, entry_id, **kwargs):
        with self._get_session() as session:
            entry = session.query(Entry).get(entry_id)
            if entry:
                for key, value in kwargs.items():
                    if hasattr(entry, key):
                        setattr(entry, key, value)
                session.commit()
                self.entry_updated.emit(entry)

    def delete_entry(self, entry_id):
        with self._get_session() as session:
            entry = session.query(Entry).get(entry_id)
            if entry:
                session.delete(entry)
                session.commit()
                self.entry_deleted.emit(entry_id)

    def get_entries_by_section(self, section_id):
        with self._get_session() as session:
            return session.query(Entry).filter(Entry.section_id == section_id).order_by(Entry.lecture_date).all()

    # ----- Файлы и привязка -----
    def attach_file(self, entry_id, source_path, original_name=None):
        """
        Копирует файл в хранилище, создаёт запись File и привязывает к Entry.
        Возвращает FileLink.
        """
        source = Path(source_path)
        if not source.is_file():
            raise FileNotFoundError(f"Файл {source_path} не найден")

        # Генерируем уникальное имя в хранилище
        ext = source.suffix
        dest_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{source.stem}{ext}"
        dest_path = self._storage_dir / dest_name
        shutil.copy2(source, dest_path)

        # Определяем MIME-тип (упрощённо)
        mime = self._guess_mime(dest_path)

        with self._get_session() as session:
            file_obj = File(
                original_name=original_name or source.name,
                stored_path=str(dest_path.relative_to(self._storage_dir.parent)),
                mime_type=mime,
                size=dest_path.stat().st_size
            )
            session.add(file_obj)
            session.flush()  # чтобы получить file_obj.id

            link = FileLink(
                file_id=file_obj.id,
                entry_id=entry_id,
                link_type='attachment',
                order=session.query(FileLink).filter(FileLink.entry_id == entry_id).count()
            )
            session.add(link)
            session.commit()
            self.file_attached.emit(entry_id, file_obj.id)
            return link

    def _guess_mime(self, path):
        ext = path.suffix.lower()
        mime_map = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
            '.pdf': 'application/pdf', '.txt': 'text/plain', '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        return mime_map.get(ext, 'application/octet-stream')

    # ----- Поиск по заметкам (базовый) -----
    def search_notes(self, keyword):
        with self._get_session() as session:
            # Поиск по полю note (case-insensitive)
            results = session.query(Entry).filter(Entry.note.contains(keyword)).all()
            return results

    # ----- Работа с метаданными фото (пункт 6) -----
    @staticmethod
    def extract_photo_date(file_path):
        try:
            img = Image.open(file_path)
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        # формат "2025:04:10 14:30:00"
                        return datetime.strptime(value[:10], '%Y:%m:%d').date()
            return None
        except Exception:
            return None

    def add_photo_by_metadata(self, section_id, photo_path):
        """Добавляет фото в запись с датой из EXIF (создаёт запись при необходимости)"""
        date_taken = self.extract_photo_date(photo_path)
        if not date_taken:
            # если даты нет – прикрепить к "сегодняшней" записи или создать новую
            date_taken = date.today()

        with self._get_session() as session:
            # Ищем запись в этом разделе с такой же датой и не глобальную
            entry = session.query(Entry).filter(
                Entry.section_id == section_id,
                Entry.lecture_date == date_taken,
                Entry.is_global == False
            ).first()
            if not entry:
                entry = Entry(
                    section_id=section_id,
                    lecture_date=date_taken,
                    title=f"Фото от {date_taken.isoformat()}",
                    note="Автоматически создано при добавлении фото"
                )
                session.add(entry)
                session.commit()
                self.entry_added.emit(entry)

        # Прикрепляем файл (вне сессии, т.к. attach_file открывает свою)
        self.attach_file(entry.id, photo_path)