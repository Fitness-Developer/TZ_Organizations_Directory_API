from sqlalchemy.orm import Session
from app.models.building import Building
from app.schemas.building import BuildingCreate

"""
Модуль CRUD-операций для работы со зданиями.

Содержит функции для создания зданий и получения списка всех зданий.
"""

def create_building(db: Session, building_in: BuildingCreate):
    """
     Создаёт новое здание в базе данных.

     Args:
         db (Session): активная сессия SQLAlchemy
         building_in (BuildingCreate): данные для создания здания (адрес, координаты и т.д.)

     Returns:
         Building: созданное здание
     """
    building = Building(**building_in.dict())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building

def get_buildings(db: Session):
    """
        Возвращает список всех зданий из базы данных.

        Returns:
            List[Building]: список всех зданий
    """
    return db.query(Building).all()