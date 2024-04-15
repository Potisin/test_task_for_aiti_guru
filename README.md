### Конвертер валют API

#### Эндпоинты:
1. [GET] /docs - Swagger документация.
2. [GET] /api/available-currencies/ - предоставляет список доступных валют.
3. [GET] /api/rates/ - принимает параметры from_currency, to_currency, value. 
Пример запроса: /api/rates/?from_currency=RUB&to_currency=USD&value=10000.

#### Варианты запуска:

1. ##### Docker:
Сборка и запуск с использованием Docker:
```
docker build -t test_task_for_aiti_guru .
docker run -d --name test_task_for_aiti_guru -p 8000:8000 test_task_for_aiti_guru
```

2. ##### Docker Compose:
Запуск с использованием Docker Compose:
```
docker-compose up -d --build
```

3. ##### Локальный запуск:
Запуск приложения локально:
```
python3 -m venv .venv  
source .venv/bin/activate  # для Windows используйте .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --reload
```

