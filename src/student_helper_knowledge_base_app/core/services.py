"""
data_service.py - Сервисный слой для работы с базой знаний студента.
Обеспечивает высокоуровневый API для GUI, инкапсулирует SQLAlchemy,
управление файлами и сигналы для обновления интерфейса.
"""

import shutil
import json
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional, Union, Dict, Tuple, Any

from PySide6.QtCore import QObject, Signal
from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import sessionmaker, joinedload

from src.student_helper_knowledge_base_app.core.models import init_db, Section, Entry, File, FileLink


class DataServiceError(Exception):
    """Базовое исключение для ошибок сервиса."""
    pass


class DataService(QObject):
    """
    Основной сервис для управления данными. Испускает сигналы при изменениях.
    """

    # Сигналы для разделов
    section_added = Signal(object)   # Section
    section_updated = Signal(object)
    section_deleted = Signal(int)

    # Сигналы для записей
    entry_added = Signal(object)     # Entry
    entry_updated = Signal(object)
    entry_deleted = Signal(int)

    # Сигналы для файлов
    file_attached = Signal(int, int)  # entry_id, file_id
    file_detached = Signal(int, int)  # entry_id, file_id
    file_deleted = Signal(int)        # file_id (физическое удаление)

    # Общий сигнал для сброса всех данных (смена базы)
    data_reset = Signal()

    def __init__(self, db_path: str = 'sqlite:///data/app_data.db',
                 storage_dir: Optional[Path] = None,
                 parent: Optional[QObject] = None):
        super().__init__(parent)
        self._engine, self._Session = init_db(db_path, echo=False, expire_on_commit=False)

        # Хранилище файлов
        if storage_dir is None:
            storage_dir = Path('data/storage')
        self._storage_dir = storage_dir.resolve()
        self._storage_dir.mkdir(parents=True, exist_ok=True)

        # Настройки ассоциирования приложений
        self.__init_app_settings("data/app_settings.json")

    # ======================================================================
    # Вспомогательные методы
    # ======================================================================
    def _get_session(self):
        """Возвращает новую сессию (контекстный менеджер)."""
        return self._Session()

    @staticmethod
    def _safe_commit(session, error_msg="Ошибка базы данных"):
        """Фиксирует транзакцию, при ошибке откатывает и выбрасывает DataServiceError."""
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise DataServiceError(f"{error_msg}: {e}")

    def _guess_mime(self, path: Path) -> str:
        """Определяет MIME-тип по расширению."""
        ext = path.suffix.lower()
        mime_map = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
            '.gif': 'image/gif', '.bmp': 'image/bmp', '.webp': 'image/webp',
            '.pdf': 'application/pdf', '.txt': 'text/plain',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.md': 'text/markdown', '.py': 'text/x-python', '.html': 'text/html',
        }
        return mime_map.get(ext, 'application/octet-stream')


    # ======================================================================
    # Разделы
    # ======================================================================
    def create_section(self, name: str, parent_id: Optional[int] = None) -> Section:
        with self._get_session() as session:
            section = Section(name=name, parent_section_id=parent_id)
            session.add(section)
            self._safe_commit(session, "Не удалось создать раздел")
            # Загружаем заново, чтобы получить отношения (если нужны)
            session.refresh(section)
            self.section_added.emit(section)
            return section

    def update_section(self, section_id: int, **kwargs) -> Optional[Section]:
        with self._get_session() as session:
            section = session.query(Section).get(section_id)
            if not section:
                return None
            for key, value in kwargs.items():
                if hasattr(section, key):
                    setattr(section, key, value)
            self._safe_commit(session, "Не удалось обновить раздел")
            session.refresh(section)
            self.section_updated.emit(section)
            return section

    def delete_section(self, section_id: int) -> bool:
        with self._get_session() as session:
            section = session.query(Section).get(section_id)
            if not section:
                return False
            # Удаляем каскадом (записи, связи, файлы? файлы не удаляем)
            session.delete(section)
            self._safe_commit(session, "Не удалось удалить раздел")
            self.section_deleted.emit(section_id)
            return True

    def get_sections(self, parent_id: Optional[int] = None) -> List[Section]:
        with self._get_session() as session:
            query = session.query(Section)
            if parent_id is None:
                query = query.filter(Section.parent_section_id.is_(None))
            else:
                query = query.filter(Section.parent_section_id == parent_id)
            return query.order_by(Section.name).all()

    def get_section_by_id(self, section_id: int) -> Optional[Section]:
        with self._get_session() as session:
            return session.query(Section).get(section_id)


    # ======================================================================
    # Записи
    # ======================================================================
    def create_entry(self, section_id: int,
                     lecture_date: Optional[date] = None,
                     is_global: bool = False,
                     title: Optional[str] = None,
                     note: Optional[str] = None) -> Entry:
        with self._get_session() as session:
            # Проверяем существование раздела
            section = session.query(Section).get(section_id)
            if not section:
                raise DataServiceError(f"Раздел с id={section_id} не существует")

            entry = Entry(
                section_id=section_id,
                lecture_date=lecture_date,
                is_global=is_global,
                title=title,
                note=note
            )
            session.add(entry)
            self._safe_commit(session, "Не удалось создать запись")
            session.refresh(entry)
            self.entry_added.emit(entry)
            return entry

    def update_entry(self, entry_id: int, **kwargs) -> Optional[Entry]:
        with self._get_session() as session:
            entry = session.query(Entry).get(entry_id)
            if not entry:
                return None
            for key, value in kwargs.items():
                if hasattr(entry, key):
                    setattr(entry, key, value)
            self._safe_commit(session, "Не удалось обновить запись")
            session.refresh(entry)
            self.entry_updated.emit(entry)
            return entry

    def ensure_entry_by_date(self, section_id: int, date: date, title=None, note=None) -> Entry:
        """Находит запись в разделе по дате или создаёт новую."""
        with self._get_session() as session:
            entry = session.query(Entry).filter(
                Entry.section_id == section_id,
                Entry.lecture_date == date,
                Entry.is_global == False
            ).first()
            if not entry:
                entry = Entry(
                    section_id=section_id,
                    lecture_date=date,
                    title=title,
                    note=(note or "Автоматически созданная запись")
                )
                session.add(entry)
                self._safe_commit(session, f"Не удалось создать запись для даты {date}")
                session.refresh(entry)
                self.entry_added.emit(entry)
            return entry

    def delete_entry(self, entry_id: int) -> bool:
        with self._get_session() as session:
            entry = session.query(Entry).get(entry_id)
            if not entry:
                return False
            # Удаляем все FileLink связанные с этой записью (каскад)
            # Физические файлы НЕ удаляем, они могут быть привязаны к другим записям
            session.delete(entry)
            self._safe_commit(session, "Не удалось удалить запись")
            self.entry_deleted.emit(entry_id)
            return True

    def get_entries_by_section(self, section_id: int) -> List[Entry]:
        with self._get_session() as session:
            return (session.query(Entry)
                    .filter(Entry.section_id == section_id)
                    .order_by(Entry.lecture_date.desc(), Entry.created_at.desc())
                    .all())

    def get_entry_by_id(self, entry_id: int) -> Optional[Entry]:
        with self._get_session() as session:
            return session.query(Entry).get(entry_id)

    def get_dates_with_entries(self, section_id: int) -> List[date]:
        with self._get_session() as session:
            dates = session.query(Entry.lecture_date).filter(
                Entry.section_id == section_id,
                Entry.lecture_date.isnot(None)
            ).distinct().all()
            return [d[0] for d in dates if d[0] is not None]

    def search_notes(self, keyword: str) -> List[Entry]:
        """Простой поиск по полю note (case-insensitive)."""
        if not keyword.strip():
            return []
        with self._get_session() as session:
            return session.query(Entry).filter(
                func.lower(Entry.note).contains(keyword.lower())
            ).order_by(Entry.created_at.desc()).all()


    # ======================================================================
    # Файлы и привязка (с полиморфными владельцами)
    # ======================================================================
    def _store_file(self, source_path: Path, original_name: str) -> Path:
        """Копирует файл в хранилище и возвращает относительный путь."""
        ext = source_path.suffix.lower()
        # Генерируем уникальное имя: timestamp_оригинальное_имя
        base = source_path.stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{timestamp}_{base}{ext}"
        dest_path = self._storage_dir / new_name
        shutil.copy2(source_path, dest_path)
        # Возвращаем путь относительно корня storage_dir
        return dest_path.relative_to(self._storage_dir.parent)

    def add_file(self, source_path: Union[str, Path],
                 original_name: Optional[str] = None) -> File:
        """
        Добавляет файл в хранилище и создаёт запись File (без привязки к записи).
        Возвращает объект File (в detached состоянии).
        """
        source = Path(source_path)
        if not source.is_file():
            raise DataServiceError(f"Файл не найден: {source_path}")

        orig_name = original_name if original_name else source.name
        rel_path = self._store_file(source, orig_name)
        mime = self._guess_mime(source)
        size = source.stat().st_size

        with self._get_session() as session:
            file_obj = File(
                original_name=orig_name,
                stored_path=str(rel_path),
                mime_type=mime,
                size=size
            )
            session.add(file_obj)
            self._safe_commit(session, "Не удалось добавить файл")
            session.refresh(file_obj)
            return file_obj  # в detached состоянии

    def update_file(self, file_id: int, **kwargs) -> Optional[File]:
        with self._get_session() as session:
            file_obj = session.query(File).get(file_id)
            if not file_obj:
                return None
            for key, value in kwargs.items():
                if hasattr(file_obj, key):
                    setattr(file_obj, key, value)
            self._safe_commit(session, "Не удалось обновить файл")
            session.refresh(file_obj)
            return file_obj

    def attach_file_to_entry(self, entry_id: int, file_id: int,
                             link_type: str = 'attachment',
                             order_in_entry: Optional[int] = None) -> FileLink:
        """
        Привязывает существующий файл к записи (прямая привязка, без владельца).
        """
        with self._get_session() as session:
            entry = session.query(Entry).get(entry_id)
            if not entry:
                raise DataServiceError(f"Запись {entry_id} не найдена")

            file_obj = session.query(File).get(file_id)
            if not file_obj:
                raise DataServiceError(f"Файл {file_id} не найден")

            # Определяем order_in_entry, если не задан
            if order_in_entry is None:
                max_order = session.query(func.max(FileLink.order_in_entry)).filter(
                    FileLink.entry_id == entry_id
                ).scalar()
                order_in_entry = (max_order or 0) + 1

            link = FileLink(
                entry_id=entry_id,
                owner_type=None,
                owner_id=None,
                file_id=file_id,
                link_type=link_type,
                order_in_entry=order_in_entry,
                order_in_owner=None
            )
            session.add(link)
            self._safe_commit(session, "Не удалось прикрепить файл к записи")
            session.refresh(link)
            self.file_attached.emit(entry_id, file_id)
            return link

    def attach_file_to_owner(self, entry_id: int, owner_type: str, owner_id: int,
                             file_id: int, link_type: str = 'attachment',
                             order_in_entry: Optional[int] = None,
                             order_in_owner: Optional[int] = None) -> FileLink:
        """
        Привязывает файл к конкретному владельцу (блоку, аннотации и т.д.).
        Владелец должен принадлежать указанной записи.
        """
        with self._get_session() as session:
            entry = session.query(Entry).get(entry_id)
            if not entry:
                raise DataServiceError(f"Запись {entry_id} не найдена")

            # Определяем order_in_entry (глобальный порядок)
            if order_in_entry is None:
                max_order = session.query(func.max(FileLink.order_in_entry)).filter(
                    FileLink.entry_id == entry_id
                ).scalar()
                order_in_entry = (max_order or 0) + 1

            # Определяем order_in_owner (локальный порядок внутри владельца)
            if order_in_owner is None:
                max_owner_order = session.query(func.max(FileLink.order_in_owner)).filter(
                    FileLink.owner_type == owner_type,
                    FileLink.owner_id == owner_id
                ).scalar()
                order_in_owner = (max_owner_order or 0) + 1

            link = FileLink(
                entry_id=entry_id,
                owner_type=owner_type,
                owner_id=owner_id,
                file_id=file_id,
                link_type=link_type,
                order_in_entry=order_in_entry,
                order_in_owner=order_in_owner
            )
            session.add(link)
            self._safe_commit(session, "Не удалось прикрепить файл к владельцу")
            session.refresh(link)
            self.file_attached.emit(entry_id, file_id)
            return link

    def add_n_attach_file_to_entry(self, file_path: Union[str, Path], entry_id: int,
                                   link_type='attachment') -> File:
        """Копирует файл в хранилище, создает запись File и прикрепляет к указанной записи"""
        file_obj = self.add_file(file_path)
        self.attach_file_to_entry(entry_id, file_obj.id, link_type=link_type)
        return file_obj

    def delete_file_permanently(self, file_id: int, physical_delete: bool = True) -> None:
        """
        Полностью удаляет файл из хранилища и из БД.
        Все связанные FileLink удаляются каскадно благодаря ondelete='CASCADE'.
        """
        with self._get_session() as session:
            file_obj = session.query(File).get(file_id)
            if not file_obj:
                return
            # Удаляем физический файл, если подтверждено
            if physical_delete:
                full_path = (self._storage_dir.parent / file_obj.stored_path).resolve()
                if full_path.exists():
                    full_path.unlink()
            session.delete(file_obj)
            self._safe_commit(session, "Не удалось удалить файл")
            self.file_deleted.emit(file_id)

    def check_file_orphaned(self, file_id: int) -> bool:
        """Проверяет, остались ли ссылки на файл"""
        with self._get_session() as session:
            # Получаем количество ссылок на файл
            remaining = session.query(FileLink).filter_by(file_id=file_id).count()
            if remaining == 0:
                # Ссылок нет - файл стал сиротой
                return True
        return False

    def detach_file(self, entry_id: int, file_id: int,
                    auto_delete_orphaned: bool = False,
                    physical_delete: bool = True) -> Tuple[bool, bool]:
        """
        Отвязывает файл от конкретной записи (удаляет запись FileLink).
        Если auto_delete_orphaned=True и после отвязки у файла не осталось ссылок,
        файл полностью удаляется (физически и из БД).
        Возвращает: (True, X), если файл был отвязан, (X, True) — если был удален.
        """
        with self._get_session() as session:
            link = session.query(FileLink).filter_by(
                entry_id=entry_id, file_id=file_id
            ).first()
            if not link:
                return False, False
            session.delete(link)
            self._safe_commit(session, "Не удалось отвязать файл")
            self.file_detached.emit(entry_id, file_id)

        # Если указано, проверяем, остались ли ссылки на этот файл и удаляем, если файл осиротел
        if auto_delete_orphaned and self.check_file_orphaned(file_id):
            self.delete_file_permanently(file_id, physical_delete)
            return True, True
        return True, False

    def get_files_for_entry(self, entry_id: int) -> List[File]:
        """Возвращает все файлы, привязанные к записи (любым способом)."""
        with self._get_session() as session:
            # Используем joinedload для оптимизации
            links = (session.query(FileLink)
                     .filter(FileLink.entry_id == entry_id)
                     .options(joinedload(FileLink.file))
                     .order_by(FileLink.order_in_entry)
                     .all())
            return [link.file for link in links if link.file.deleted_at is None]

    def get_files_for_owner(self, owner_type: str, owner_id: int) -> List[File]:
        """Возвращает файлы, привязанные к конкретному владельцу."""
        with self._get_session() as session:
            links = (session.query(FileLink)
                     .filter(FileLink.owner_type == owner_type,
                             FileLink.owner_id == owner_id)
                     .order_by(FileLink.order_in_owner)
                     .all())
            return [link.file for link in links if link.file.deleted_at is None]

    def cleanup_unused_files(self, physical_delete: bool = True) -> int:
        """
        Удаляет записи файлов, на которые нет ни одной ссылки (FileLink).
        Если physical_delete=True, также удаляет физические файлы с диска.
        Возвращает количество удалённых файлов.
        """
        deleted_count = 0
        with self._get_session() as session:
            # Находим файлы без активных связей (и не помеченные как удалённые, если не нужны)
            subq = session.query(FileLink.file_id).distinct().subquery()
            unused_files = session.query(File).filter(File.id.notin_(subq))

            for file_obj in unused_files:
                if physical_delete:
                    full_path = self._storage_dir / file_obj.stored_path
                    if full_path.exists():
                        full_path.unlink()
                session.delete(file_obj)
                deleted_count += 1
                self.file_deleted.emit(file_obj.id)

            self._safe_commit(session, "Ошибка при очистке неиспользуемых файлов")
        return deleted_count

    def soft_delete_file(self, file_id: int) -> bool:
        """Помечает файл как удалённый (мягкое удаление)."""
        with self._get_session() as session:
            file_obj = session.query(File).get(file_id)
            if not file_obj:
                return False
            file_obj.deleted_at = datetime.now()
            self._safe_commit(session, "Не удалось пометить файл как удалённый")
            return True

    def restore_file(self, file_id: int) -> bool:
        """Восстанавливает файл из мягкого удаления."""
        with self._get_session() as session:
            file_obj = session.query(File).get(file_id)
            if not file_obj:
                return False
            file_obj.deleted_at = None
            self._safe_commit(session, "Не удалось восстановить файл")
            return True

    def get_file_path(self, file_id: int) -> Optional[Path]:
        """Возвращает абсолютный путь к файлу в хранилище."""
        with self._get_session() as session:
            file_obj = session.query(File).get(file_id)
            if not file_obj or file_obj.deleted_at is not None:
                return None
            return (self._storage_dir.parent / file_obj.stored_path).resolve()


    # ======================================================================
    # Специализированный метод: добавление фото по метаданным
    # ======================================================================
    @staticmethod
    def extract_photo_date(file_path: Union[str, Path]) -> Optional[date]:
        """Извлекает дату съёмки из EXIF (Pillow)."""
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            img = Image.open(file_path)
            exif = img._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        # формат "2025:04:10 14:30:00"
                        date_str = value.split()[0]
                        return datetime.strptime(date_str, '%Y:%m:%d').date()
            return None
        except Exception:
            return None

    def add_photo_to_entry_by_file(self, photo_path: Union[str, Path], entry_id: int) -> File:
        """
        Копирует фото в хранилище и прикрепляет к указанной записи
        (для API и промежуточной логики, сейчас практически аналог add_n_attach_file_to_entry).
        """
        return self.add_n_attach_file_to_entry(photo_path, entry_id, 'photo')

    def _add_photo_by_metadata(self, section_id: int, photo_path: Union[str, Path]) -> Tuple[File, Entry, date]:
        """
        Добавляет фото в запись, соответствующую дате съёмки.
        Если запись с такой датой отсутствует, создаёт новую.
        Возвращает запись, к которой привязано фото.
        """
        photo_path = Path(photo_path)
        photo_date = self.extract_photo_date(photo_path)
        if not photo_date:
            raise DataServiceError("Не удалось извлечь дату из EXIF")
            #photo_date = date.today()  # или можно выбросить исключение

        # Сначала найдём или создадим запись
        entry = self.ensure_entry_by_date(section_id, photo_date,
                                          note="Автоматически создано при добавлении фото по EXIF")

        # Теперь добавляем файл и привязываем
        try:
            # Добавляем файл и прикрепляем к записи пока без метаданных
            file_obj = self.add_photo_to_entry_by_file(photo_path, entry.id)
            # Добавляем в метаданные в metadata_json флаг "добавлен автоматически"
            file_obj.metadata_json = json.dumps({"auto_added": True})
            self.update_file(file_obj.id, metadata_json=file_obj.metadata_json)
        except DataServiceError as e:
            # Если файл уже существует? При любой ошибке пробрасываем исключение
            raise DataServiceError(f"Не удалось прикрепить фото: {e}")
        return file_obj, entry, photo_date

    def add_photos_batch_to_section(self, photo_paths: List[Union[str, Path]], section_id: int) -> Dict[str, List]:
        """
        Обрабатывает список фото.
        Возвращает словарь:
        {
            'added': [(entry_id, file_id, date), ...],
            'failed': [(file_path, error_message), ...]
        }
        Для failed файлов дата не извлечена.
        """
        from collections import defaultdict
        result = {'added': [], 'failed': []}

        for path in photo_paths:
            path = Path(path)
            try:
                file_obj, entry, photo_date = self._add_photo_by_metadata(section_id, path)
                result['added'].append((entry.id, file_obj.id, photo_date))
            except Exception as e:
                result['failed'].append((str(path), str(e)))
        return result


    # ======================================================================
    # Управление настройками внешних программ (для пункта 3)
    # ======================================================================
    # Здесь просто хранилище в отдельной таблице или в QSettings.
    # Реализуем просто через словарь в памяти с сохранением в JSON-файл.
    def __init_app_settings(self, path: Union[str, Path]):
        self._app_settings_path = Path(path)
        self._app_settings = {}
        if self._app_settings_path.exists():
            try:
                with open(self._app_settings_path, 'r', encoding='utf-8') as f:
                    self._app_settings = json.load(f)
            except:
                pass

    def get_associated_app(self, mime_type: str) -> Optional[str]:
        """Возвращает путь к приложению, ассоциированному с MIME-типом."""
        return self._app_settings.get(mime_type)

    def set_associated_app(self, mime_type: str, app_path: str):
        """Устанавливает приложение для открытия файлов данного MIME-типа."""
        self._app_settings[mime_type] = app_path
        with open(self._app_settings_path, 'w', encoding='utf-8') as f:
            json.dump(self._app_settings, f, indent=2)

    # ======================================================================
    # Закрытие ресурсов
    # ======================================================================
    def close(self):
        """Закрывает соединение с БД (если нужно)."""
        self._engine.dispose()