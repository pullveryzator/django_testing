# Django Testing Project

Этот проект предназначен для тестирования двух Django-приложений: **yanews** и **yanote**. В проекте используются два популярных инструмента для тестирования: **unittest** и **pytest**.

## Структура проекта

- **Dev/**
  - **django_testing/** — корневая директория проекта.
    - **ya_news/** — проект `yanews`.
      - **news/** — приложение для управления новостями.
        - `fixtures/` — фикстуры для базы данных.
        - `migrations/` — миграции базы данных.
        - **tests/** — тесты unittest.
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
        - **pytest_tests/** — директория с тестами pytest для `yanote`.
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
Инструкции по запуску проектов Ya_News и Ya_Note и тестов к ним **аналогичны друг другу**. Ниже приведена инструкция для Ya_News.
1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/pullveryzator/django_testing.git
   cd django_testing
3. **Создайте и активируйте виртуальное окружение**:
- Перейдите в директорию с файлом manage.py:
   ```bash
   cd YaNews/ya_news/
- Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   venv\Scripts\activate     # Для Windows
5. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
6. **Создайте и примените миграции**:
   ```bash
   cd YaNews/ya_news/
   python manage.py makemigrations
   python manage.py migrate
7. **Cоздайте суперпользователя**:
   ```bash
   python manage.py createsuperuser.
8. **Для заполнения базы данных новостями, выполните команду**:
   ```bash
   python manage.py loaddata news.json
9. **Запустите сервер**:
   ```bash
   cd YaNews/ya_news/
   python manage.py runserver
## Тестирование

**Тестирование ya_news через pytest**:
1. Перейдите в директорию ya_news:
   ```bash
   cd YaNews/ya_news/
2. Запустите тесты:
   ```bash
   pytest
**Тестирование ya_news через unittest**:
1. Запустите тесты:
   ```bash
   python manage.py test news.tests

## Используемые технологии
- Django: Основной фреймворк для разработки веб-приложений.

- unittest: Встроенный фреймворк для тестирования (используется в yanote).

- pytest: Альтернативный фреймворк для тестирования (используется в yanews).

- SQLite: База данных для разработки.

## Лицензия
- Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.

## Авторы
- https://github.com/pullveryzator
