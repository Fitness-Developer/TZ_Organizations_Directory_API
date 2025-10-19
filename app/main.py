from fastapi import FastAPI
from app.routers import organizations, building, activity

app = FastAPI(
    title="Organizations Directory API",
    version="1.0.0",
    description="""
**Organizations Directory API**

API для управления организациями, зданиями и видами деятельности.

### Возможности:
- Получение организаций по координатам, зданиям и видам деятельности  
- Управление организациями и связанными объектами  
- Поиск по вложенным видам деятельности (родительским и дочерним)

Документация:
- Swagger UI — `/docs`  
- ReDoc — `/redoc`
    """
)

# Подключаем роутеры
app.include_router(organizations.router)
app.include_router(building.router)
app.include_router(activity.router)

@app.get("/", tags=["Health"], summary="Проверка состояния API")
def root():
    """Простой health-check, чтобы убедиться, что сервер работает."""
    return {"status": "ok", "message": "Organizations Directory API is running 🚀"}











