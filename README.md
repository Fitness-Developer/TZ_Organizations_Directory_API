# Тестовое задание "Создание REST API" приложения

Стак проекта:
- FastAPI
- PostgreSQL
- sqlalchemy + alembic
- pydantic
- Docker


Функционал:
- CRUD для организаций, зданий и видов деятельности.
- Организация может иметь: название, несколько номеров телефонов, привязку к конкретному зданию, несколько видов деятельности
- Здание содержит: адрес, географические координаты (широта и долгота), деятельность может быть вложенной (до 3 уровней).
- Фильтры и поиск:
  - Список всех организаций в здании
  - Список организаций по виду деятельности (включая вложенные)
  - Поиск организаций по названию
  - Поиск по радиусу или прямоугольной области на карте
- Статический API ключ для взаимодействия с сервером.
- Все ответы в формате JSON.
- Документация Swagger UI / Redoc.


## Структура проекта
```
TZsecunda/
├── alembic/                   
│   └── ...                     # Каталог для миграций базы данных, создаваемых Alembic
├── app/
│   ├── main.py                 # Точка входа FastAPI приложения. Здесь создается экземпляр FastAPI, подключаются роутеры и middleware
│   ├── database.py             # Настройка подключения к PostgreSQL через SQLAlchemy, создание сессий
│   ├── dependencies.py         # Общие зависимости для маршрутов (Depends), например получение DB-сессии
│   ├── crud/                   # Папка с бизнес-логикой и операциями CRUD
│   │   ├── organizations.py    # CRUD-операции для организаций (создание, получение, фильтры)
│   │   ├── buildings.py        # CRUD-операции для зданий
│   │   └── activities.py       # CRUD-операции для видов деятельности
│   │
│   ├── models/                 # Модели базы данных (SQLAlchemy)
│   │   ├── organizations.py    # Модель организации
│   │   ├── buildings.py        # Модель здания
│   │   └── activities.py       # Модель вида деятельности
│   │
│   ├── routers/                # Роутеры FastAPI — здесь определяются эндпоинты
│   │   ├── organizations.py    # Эндпоинты для организаций (GET, POST, поиск и т.д.)
│   │   ├── buildings.py        # Эндпоинты для зданий
│   │   └── activities.py       # Эндпоинты для видов деятельности
│   │
│   └── schemas/                # Pydantic-схемы для валидации и сериализации данных
│       ├── organization.py     # Схемы OrganizationCreate, OrganizationOut и т.д.
│       ├── building.py         # Схемы для здания
│       └── activity.py         # Схемы для вида деятельности
│
├── alembic.ini                 # Основной конфигурационный файл Alembic для миграций базы данных
├── docker-compose.yml          # Конфигурация Docker Compose для запуска всех сервисов (FastAPI, PostgreSQL и др.)
├── requirements.txt            # Список Python-зависимостей проекта
└── Dockerfile                  # Инструкция для сборки Docker-образа приложения
```

## Запуск проекта

1. Клонируем репозиторий - 
```
git clone https://github.com/Fitness-Developer/TZ_Organizations_Directory_API.git
cd TZ_Organizations_Directory_API
```
2. Создаем файл .env с настройками подключения к БД - 
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=orgs_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/orgs_db
```
3. Запуск через Docker Compose:
```
docker-compose up --build
```
4. Если меняли структуру БД или миграции, сбросить старые данные:
```
docker-compose down -v
docker-compose up --build
```

Сервер будет доступен по адресу - http://localhost:8000

## Api Endpoints
Организации:
- POST /organizations — создать организацию
- GET /organizations/all_organizations — получить список всех организаций
- GET /organizations/by_building_id/{building_id} — получить организации в конкретном здании
- GET /organizations/by_activity/{activity} — получить организации по виду деятельности
- GET /organizations/by_coordinates/ — получить организации по координатам (широта, долгота)
- GET /organizations/by_organization_id/{organization_id} — получить организацию по ID
- GET /organizations/by_organization_name/{organization_name} — получить организацию по названию
- GET /organizations/by_activity_name/{activity_name} — получить организации по виду деятельности с учётом иерархии


Здания:
- GET /buildings — список зданий
- POST /buildings — создать здание

Деятельность:
- GET /activities — список видов деятельности
- POST /activities — создать вид деятельности
- Поддержка вложенности до 3 уровней

Документация:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc


