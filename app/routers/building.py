from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.building import BuildingCreate, BuildingOut
from app.crud.building import create_building, get_buildings

router = APIRouter(prefix="/buildings", tags=["Buildings"])

# -------------------------------------------------------------------------
# Создание нового здания
# -------------------------------------------------------------------------
@router.post(
    "/",
    response_model=BuildingOut,
    summary="Создать здание",
    description="""
Добавляет новое здание в базу данных.  
Необходимо указать **адрес**, **широту** и **долготу**.
"""
)
def create_building_endpoint(building_in: BuildingCreate, db: Session = Depends(get_db)):
    try:
        building = create_building(db, building_in)
        return building
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании здания: {str(e)}"
        )

# -------------------------------------------------------------------------
# Получить список всех зданий
# -------------------------------------------------------------------------
@router.get(
    "/",
    response_model=List[BuildingOut],
    summary="Получить все здания",
    description="Возвращает список всех зданий, зарегистрированных в системе."
)
def get_all_buildings(db: Session = Depends(get_db)):
    buildings = get_buildings(db)
    if not buildings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здания не найдены"
        )
    return buildings