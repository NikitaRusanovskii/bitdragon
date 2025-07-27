# BitDragon/Tracker

Трекер - REST API сервис, реализованный на python + fastapi, отвечающий за регистрацию и отслеживание раздач.

## Описание:
    Tracker предоставляет API для управления мета-файлами и пирами.
    Функционал:
    - Регистрация новых раздач
    - Получение списка пиров для мета-файла
    - Обновление информации о пирах
    - Удаление раздач
    - Загрузка и выгрузка мета-файлов

## Структура проекта:
    tracker/
    ---- tracker.py # Точка входа в FastAPI-приложение
    ---- models.py # Модели данных (SQLModel)
    ---- db_config # Конфигурация подключения к базе данных.
    ---- meta_files/ # Каталог для хранения мета-файлов
    ---- README.md # Вы здесь :D

## Запуск на локальном сервере:
    1. Создаём виртуальное окружение.
        python -m venv venv
    
    2. Активируем его.
        source venv/bin/activate # Linux/macOS
        venv\Scripts\activate.bat # Windows

    3. Устанавливаем зависимости.
        pip install -r requirements.txt

    4. Запускаем приложение.
        uvicorn tracker:app --reload

    ---- API будет доступен по адресу http://127.0.0.1:8000 ----

## Примеры запросов

    1. Получить список всех мета-файлов:
    GET /meta_files
    2. Скачать мета-файл:
    GET /meta_files/{file_name}
    3. Загрузить мета-файл:
    POST /upload/
    Content-Type: multipart/form-data
    file: [выбрать файл]
    4. Зарегестрировать раздачу:
    POST /register
    Content-Type: application/json
    {
        "meta_file": "example.bit",
        "peers": ["193.114.32.1:5320", "192.118.110.3:5320"]
    }
