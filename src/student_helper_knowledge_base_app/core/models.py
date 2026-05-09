"""
Модели данных для MVP приложения «База знаний студента».
Используется SQLAlchemy (declarative) + SQLite.
В дальнейшем поле `Entry.note` будет дополнено системой блоков (ContentBlock),
но останется для быстрых заметок и обратной совместимости.
"""

from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Базовый класс для всех моделей
Base = declarative_base()

# ------------------------------------------------------------
# Модель "Раздел" (учебная дисциплина)
# ------------------------------------------------------------
class Section(Base):
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    parent_section_id = Column(Integer, ForeignKey('sections.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Отношения
    parent = relationship('Section', remote_side=[id], backref='children')
    entries = relationship('Entry', back_populates='section', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Section(id={self.id}, name='{self.name}')>"


# ------------------------------------------------------------
# Модель "Запись" (лекция, практика, глобальный материал)
# ------------------------------------------------------------
class Entry(Base):
    __tablename__ = 'entries'
    __table_args__ = (
        CheckConstraint(
            "(is_global = 1 OR lecture_date IS NOT NULL)",
            name="ck_entry_has_date_if_not_global"
        ),
    )

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    lecture_date = Column(Date, nullable=True)          # дата занятия (обязательна, если is_global=0)
    is_global = Column(Boolean, default=False)          # глобальная запись (учебник и т.п.)
    title = Column(String(300), nullable=True)          # может быть пустым – тогда показываем дату
    note = Column(Text, nullable=True)                  # текстовая заметка (индексируется)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Отношения
    section = relationship('Section', back_populates='entries')
    file_links = relationship('FileLink', back_populates='entry', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Entry(id={self.id}, title='{self.title}', date={self.lecture_date})>"


# ------------------------------------------------------------
# Модель "Физический файл"
# ------------------------------------------------------------
class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    original_name = Column(String(300), nullable=False)      # имя, которое видел пользователь
    stored_path = Column(String(500), nullable=False, unique=True)  # относительный путь в хранилище приложения
    mime_type = Column(String(100), nullable=False)          # image/jpeg, application/pdf и т.д.
    size = Column(Integer, nullable=False)                   # размер в байтах
    metadata_json = Column(Text, nullable=True)              # EXIF, дата съёмки, OCR-текст (JSON)
    created_at = Column(DateTime, default=datetime.now)

    # Отношения
    file_links = relationship('FileLink', back_populates='file', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<File(id={self.id}, name='{self.original_name}')>"


# ------------------------------------------------------------
# Модель "Привязка файла к записи"
# ------------------------------------------------------------
class FileLink(Base):
    __tablename__ = 'file_links'
    __table_args__ = (
        UniqueConstraint('entry_id', 'order', name='uq_filelink_entry_order'),
    )

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id', ondelete='CASCADE'), nullable=False)
    entry_id = Column(Integer, ForeignKey('entries.id', ondelete='CASCADE'), nullable=False)
    link_type = Column(String(50), default='attachment')   # 'attachment', 'inline', 'gallery_item' и т.п.
    order = Column(Integer, default=0)                     # порядок в списке прикреплённых файлов
    created_at = Column(DateTime, default=datetime.now)

    # Отношения
    file = relationship('File', back_populates='file_links')
    entry = relationship('Entry', back_populates='file_links')

    def __repr__(self):
        return f"<FileLink file_id={self.file_id} -> entry_id={self.entry_id}>"


# ------------------------------------------------------------
# Функция для получения сессии (удобный инициализатор БД)
# ------------------------------------------------------------
def init_db(db_path='sqlite:///data/app_data.db'):
    """
    Создаёт все таблицы и возвращает объект session.
    Рекомендуется использовать с менеджером контекста.
    """
    engine = create_engine(db_path, echo=False)  # echo=True для отладки SQL
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()