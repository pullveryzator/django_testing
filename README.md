# Django Testing Project

Этот проект предназначен для тестирования двух Django-приложений: **yanews** и **yanote**. В проекте используются два популярных инструмента для тестирования: **unittest** (для `yanote`) и **pytest** (для `yanews`).

## Структура проекта

- **Dev/**
  - **django_testing/** — корневая директория проекта.
    - **ya_news/** — проект `yanews`.
      - **news/** — приложение для управления новостями.
        - `fixtures/` — фикстуры для базы данных.
        - `migrations/` — миграции базы данных.
        - **pytest_tests/** — директория с тестами pytest для `yanews`.
        - `__init__.py`
        - `admin.py`
        - `apps.py`
        - `forms.py`
        - `models.py`
        - `urls.py`
        - `views.py`
      - `templates/` — шаблоны для отображения страниц.
      - **yanews/** — основная конфигурация проекта.
      - `manage.py` — скрипт для управления проектом.
      - `pytest.ini` — конфигурация pytest.
    - **ya_note/** — проект `yanote`.
      - **notes/** — приложение для управления заметками.
        - `migrations/` — миграции базы данных.
        - **tests/** — директория с тестами unittest для `yanote`.
        - `__init__.py`
        - `admin.py`
        - `apps.py`
        - `forms.py`
        - `models.py`
        - `urls.py`
        - `views.py`
      - `templates/` — шаблоны для отображения страниц.
      - **yanote/** — основная конфигурация проекта.
      - `manage.py` — скрипт для управления проектом.
      - `pytest.ini` — конфигурация pytest.
    - `.gitignore` — список файлов и папок, скрытых от отслеживания Git.
    - `README.md` — описание проекта.
    - `requirements.txt` — список зависимостей проекта.
    - `structure_test.py` — тесты для проверки структуры проекта.

## Установка и запуск проекта

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/pullveryzator/django_testing.git
   cd django_testing
