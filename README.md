## Предполагаемая структура проекта:

```
knowledge_base_app/
├── src/                        # Исходный код
│   ├── gui/                    # Модули интерфейса
│   │   ├── main_window.py
│   │   ├── widgets/            # Кастомные виджеты (граф, просмотрщик файлов)
│   │   └── resources/          # Иконки, темы QSS
│   ├── core/                   # Основная логика
│   │   ├── data_manager.py     # Работа с БД
│   │   ├── search_engine.py    # Полнотекстовый поиск
│   │   ├── knowledge_graph.py  # Управление графом (NetworkX)
│   │   ├── file_handlers/      # Обработчики разных типов файлов
│   │   │   ├── pdf_handler.py  # (PyMuPDF)
│   │   │   ├── docx_handler.py
│   │   │   └── image_handler.py# (Pillow + EXIF)
│   │   └── external_apps.py    # Управление внешними приложениями
│   ├── models/                 # SQLAlchemy или dataclasses моделей
│   │   ├── section.py
│   │   ├── entry.py
│   │   └── file_attachment.py
│   └── utils/                  # Вспомогательные утилиты
│       ├── config.py           # Настройки (путь к GIMP и т.д.)
│       └── touch_gestures.py   # Обработка жестов
├── data/                       # Пользовательские данные
│   ├── app_data.db             # Файл базы данных SQLite
│   └── storage/                # Физические файлы (PDF, изображения и т.д.)
├── tests/                      # Тесты
├── requirements.txt
└── main.py
```