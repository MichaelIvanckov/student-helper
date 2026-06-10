"""
Модели данных для приложения «База знаний студента».
Используется SQLAlchemy (declarative) + SQLite.

Включает:
- Section (разделы дисциплин)
- Entry (записи: лекции, практики, глобальные материалы)
- File (физические файлы с поддержкой мягкого удаления)
- FileLink (полиморфные привязки файлов к записям и их составным частям с двумя уровнями сортировки)
"""

from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean, DateTime, Date,
    ForeignKey, UniqueConstraint, CheckConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base as declarative_base_
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


# Базовый класс для всех моделей
Base = declarative_base()


# ------------------------------------------------------------
# Модель "Раздел" (учебная дисциплина)
# ------------------------------------------------------------
class Section(Base):
    """Раздел (учебная дисциплина)"""
    __tablename__ = 'sections'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    parent_section_id = Column(Integer, ForeignKey('sections.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Отношения
    parent = relationship('Section', remote_side=[id], backref='children')
    entries = relationship('Entry', back_populates='section', cascade='all, delete-orphan')
    topics = relationship('Topic', back_populates='section', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Section(id={self.id}, name='{self.name}')>"


# ------------------------------------------------------------
# Модель "Запись" (лекция, практика, глобальный материал)
# ------------------------------------------------------------
class Entry(Base):
    """Запись (лекция, практика, глобальный материал)"""
    __tablename__ = 'entries'
    __table_args__ = (
        CheckConstraint(
            "(is_global = 1 OR lecture_date IS NOT NULL)",
            name="ck_entry_has_date_if_not_global"
        ),
        Index('idx_entry_complete', 'is_complete'),   # новый индекс для фильтрации
    )

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    lecture_date = Column(Date, nullable=True)          # дата занятия (обязательна, если is_global=0)
    is_global = Column(Boolean, default=False)          # глобальная запись (учебник и т.п.)
    title = Column(String(300), nullable=True)          # может быть пустым – тогда показываем дату
    note = Column(Text, nullable=True)                  # текстовая заметка (индексируется)
    is_complete = Column(Boolean, default=False, nullable=False)  # завершена ли запись
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Отношения
    section = relationship('Section', back_populates='entries')
    file_links = relationship('FileLink', back_populates='entry', cascade='all, delete-orphan')
    topics = relationship('Topic', secondary='entry_topics', back_populates='entries')

    def __repr__(self):
        return f"<Entry(id={self.id}, title='{self.title}', date={self.lecture_date}, complete={self.is_complete})>"


# ------------------------------------------------------------
# Модель "Физический файл"
# ------------------------------------------------------------
class File(Base):
    """Физический файл в хранилище с поддержкой мягкого удаления"""
    __tablename__ = 'files'
    __table_args__ = (
        Index('idx_files_deleted_at', 'deleted_at'),   # индекс для мягкого удаления
    )

    id = Column(Integer, primary_key=True)
    original_name = Column(String(300), nullable=False)      # имя, которое видел пользователь
    stored_path = Column(String(500), nullable=False, unique=True)  # относительный путь в хранилище приложения
    mime_type = Column(String(100), nullable=False)          # image/jpeg, application/pdf и т.д.
    size = Column(Integer, nullable=False)                   # размер в байтах
    metadata_json = Column(Text, nullable=True)              # EXIF, дата съёмки, OCR-текст (JSON) и пр.
    created_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, nullable=True)  # NULL = активен, иначе дата мягкого удаления

    # Отношения
    file_links = relationship('FileLink', back_populates='file', cascade='all, delete-orphan')

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def __repr__(self):
        status = " (deleted)" if self.is_deleted else ""
        return f"<File(id={self.id}, name='{self.original_name}'{status})>"


# ------------------------------------------------------------
# Модель "Привязка файла к записи"
# ------------------------------------------------------------
class FileLink(Base):
    """
    Полиморфная привязка файла к записи и её внутренним элементам.

    Поля:
    - entry_id: всегда заполнено, определяет запись-контейнер.
    - owner_type, owner_id: опционально определяют конкретную часть записи
      (блок контента, аннотацию изображения и т.д.). Если owner_type IS NULL,
      значит файл привязан напрямую к записи (link_type='attachment').
    - link_type: тип связи (attachment, gallery_item, inline_image, annotation_image и т.д.)
    - order_in_entry: порядковый номер внутри записи (глобальная сортировка)
    - order_in_owner: порядковый номер внутри владельца (например, порядок в галерее блока)
    - metadata_json: дополнительные данные (координаты на изображении и пр.)
    """
    __tablename__ = 'file_links'
    __table_args__ = (
        # CHECK: если owner_type NULL, то owner_id тоже NULL, и наоборот
        CheckConstraint(
            "(owner_type IS NULL AND owner_id IS NULL) OR (owner_type IS NOT NULL AND owner_id IS NOT NULL)",
            name="ck_filelink_owner_consistency"
        ),
        # Уникальность порядка в пределах записи
        UniqueConstraint('entry_id', 'order_in_entry', name='uq_filelink_entry_order'),
        ## Уникальность порядка в пределах владельца (только если владелец задан)
        #UniqueConstraint('owner_type', 'owner_id', 'order_in_owner',
        #                 name='uq_filelink_owner_order',
        #                 condition=owner_type.isnot(None) & owner_id.isnot(None)),
        # Индексы для ускорения частых запросов
        Index('idx_filelink_entry', 'entry_id'),
        Index('idx_filelink_file', 'file_id'),
        Index('idx_filelink_owner', 'owner_type', 'owner_id'),
        Index('idx_filelink_link_type', 'link_type'),
    )

    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey('entries.id', ondelete='CASCADE'), nullable=False)
    owner_type = Column(String(50), nullable=True)   # 'content_block', 'image_annotation' и др.
    owner_id = Column(Integer, nullable=True)
    file_id = Column(Integer, ForeignKey('files.id', ondelete='CASCADE'), nullable=False)
    link_type = Column(String(50), nullable=False, default='attachment')
    order_in_entry = Column(Integer, default=0)
    order_in_owner = Column(Integer, nullable=True)   # NULL, если владелец не задан
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    # Отношения
    entry = relationship('Entry', back_populates='file_links')
    file = relationship('File', back_populates='file_links')

    def __repr__(self):
        owner = f"{self.owner_type}:{self.owner_id}" if self.owner_type else "direct"
        return (f"<FileLink(entry={self.entry_id}, file={self.file_id}, owner={owner}, "
                f"type={self.link_type}, order_entry={self.order_in_entry}, "
                f"order_owner={self.order_in_owner})>")


# ------------------------------------------------------------
# Частичный уникальный индекс – должен быть определён ПОСЛЕ класса
# ------------------------------------------------------------
Index('uq_filelink_owner_order',
      FileLink.owner_type, FileLink.owner_id, FileLink.order_in_owner,
      unique=True,
      sqlite_where=(FileLink.owner_type.isnot(None) & FileLink.owner_id.isnot(None)))


# ------------------------------------------------------------
# Модель "Тема" (учебная тема внутри раздела)
# ------------------------------------------------------------
class Topic(Base):
    __tablename__ = 'topics'
    __table_args__ = (
        UniqueConstraint('section_id', 'name', name='uq_topic_section_name'),
        Index('idx_topics_section', 'section_id'),
        Index('idx_topics_parent', 'parent_topic_id'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.id', ondelete='CASCADE'), nullable=False)
    parent_topic_id = Column(Integer, ForeignKey('topics.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Отношения
    section = relationship('Section', back_populates='topics')
    parent = relationship('Topic', remote_side=[id], backref='children')
    entries = relationship('Entry', secondary='entry_topics', back_populates='topics')

    def __repr__(self):
        return f"<Topic(id={self.id}, name='{self.name}', section_id={self.section_id})>"


# ------------------------------------------------------------
# Ассоциативная таблица для связи Entry <-> Topic
# ------------------------------------------------------------
class EntryTopic(Base):
    __tablename__ = 'entry_topics'
    __table_args__ = (
        UniqueConstraint('entry_id', 'topic_id', name='uq_entry_topic'),
        Index('idx_entry_topics_entry', 'entry_id'),
        Index('idx_entry_topics_topic', 'topic_id'),
    )

    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer, ForeignKey('entries.id', ondelete='CASCADE'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Отношения (опционально, для удобства)
    entry = relationship('Entry', backref='topic_links')
    topic = relationship('Topic', backref='entry_links')


# ------------------------------------------------------------
# Инициализация БД
# ------------------------------------------------------------
def init_db(db_path='sqlite:///data/app_data.db', echo=False):
    """Создаёт все таблицы и возвращает engine и sessionmaker"""
    engine = create_engine(db_path, echo=echo)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session