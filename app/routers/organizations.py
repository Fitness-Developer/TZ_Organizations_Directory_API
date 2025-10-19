from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.organizations import OrganizationCreate, OrganizationOut
from app.crud.organizations import (
    create_organization,
    get_organizations,
    get_organizations_by_building,
    get_organizations_by_name_activites,
    get_organizations_by_coordinates,
    get_organization_by_id,
    get_organization_by_name,
    get_organizations_by_activity_name,
)

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
    responses={404: {"description": "Организация не найдена"}},
)

# -------------------------------------------------------------------------
# Создание новой организации
# -------------------------------------------------------------------------
@router.post(
    "/",
    response_model=OrganizationOut,
    summary="Создать организацию",
    description="""
    Добавляет новую организацию с её зданием, телефонами и видами деятельности.
    
    Пример запроса: 
    {
      "name": "Моя компания",
      "building_id": 1,
      "phones": [
        {"phone": "+7 123 456 78 90"},
        {"phone": "+7 987 654 32 10"}
      ],
      "activity_ids": [1, 2]  # id уже существующих activities в БД, сначала добавьте activities
    }
    """
)
def create_organization_endpoint(org_in: OrganizationCreate, db: Session = Depends(get_db)):
    try:
        org = create_organization(db, org_in)
        return org
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании организации: {str(e)}"
        )


# -------------------------------------------------------------------------
# Получить список всех организаций
# -------------------------------------------------------------------------
@router.get(
    "/all_organizations",
    response_model=List[OrganizationOut],
    summary="Получить все организации",
    description="Возвращает полный список всех организаций в базе данных.",
)
def get_all_organizations(db: Session = Depends(get_db)):
    orgs = get_organizations(db)
    if not orgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организации не найдены"
        )
    return orgs


# -------------------------------------------------------------------------
# Получить организации по ID здания
# -------------------------------------------------------------------------
@router.get(
    "/by_building_id/{building_id}",
    response_model=List[OrganizationOut],
    summary="Организации по зданию",
    description="Возвращает все организации, находящиеся в указанном здании.",
)
def get_all_organizations_by_building(building_id: int, db: Session = Depends(get_db)):
    orgs = get_organizations_by_building(db, building_id)
    if not orgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"В здании с ID {building_id} организации не найдены"
        )
    return orgs


# -------------------------------------------------------------------------
# Получить организации по названию деятельности
# -------------------------------------------------------------------------
@router.get(
    "/by_activity/{activity}",
    response_model=List[OrganizationOut],
    summary="Поиск организаций по названию деятельности",
    description="Находит организации, у которых указана определённая деятельность (без учёта регистра).",
)
def get_all_organizations_by_name_activites(activity: str, db: Session = Depends(get_db)):
    orgs = get_organizations_by_name_activites(db, activity)
    if not orgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организации с видом деятельности '{activity}' не найдены"
        )
    return orgs


# -------------------------------------------------------------------------
# Получить организации по координатам
# -------------------------------------------------------------------------
@router.get(
    "/by_coordinates/",
    response_model=List[OrganizationOut],
    summary="Организации по координатам",
    description="Возвращает организации, находящиеся по указанным координатам (широта и долгота).",
)
def get_all_organizations_by_coordinates(latitude: float, longitude: float, db: Session = Depends(get_db)):
    orgs = get_organizations_by_coordinates(db, latitude, longitude)
    if not orgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организации по координатам ({latitude}, {longitude}) не найдены"
        )
    return orgs


# -------------------------------------------------------------------------
# Получить организацию по её ID
# -------------------------------------------------------------------------
@router.get(
    "/by_organization_id/{organization_id}",
    response_model=OrganizationOut,
    summary="Организация по ID",
    description="Возвращает полную информацию об организации по её уникальному идентификатору.",
)
def get_one_organization_by_id(organization_id: int, db: Session = Depends(get_db)):
    org = get_organization_by_id(db, organization_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организация с ID {organization_id} не найдена"
        )
    return org


# -------------------------------------------------------------------------
# Получить организацию по имени
# -------------------------------------------------------------------------
@router.get(
    "/by_organization_name/{organization_name}",
    response_model=OrganizationOut,
    summary="Организация по названию",
    description="Ищет организацию по точному совпадению имени.",
)
def get_one_organization_by_name(organization_name: str, db: Session = Depends(get_db)):
    org = get_organization_by_name(db, organization_name)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организация с названием '{organization_name}' не найдена"
        )
    return org


# -------------------------------------------------------------------------
# Получить организации по виду деятельности (с учётом иерархии)
# -------------------------------------------------------------------------
@router.get(
    "/by_activity_name/{activity_name}",
    response_model=List[OrganizationOut],
    summary="Организации по виду деятельности (включая дочерние виды)",
    description="""
Возвращает все организации, связанные с указанным видом деятельности, **включая дочерние и родительские** виды.

Пример:  
Если запросить `"Мясная продукция"`, то будут возвращены организации, у которых деятельность `"Мясная продукция"` или родитель `"Еда"`.
""",
)
def get_organizations_by_activity(activity_name: str, db: Session = Depends(get_db)):
    orgs = get_organizations_by_activity_name(db, activity_name)
    if not orgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организации с видом деятельности '{activity_name}' не найдены"
        )
    return orgs