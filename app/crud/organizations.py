from sqlalchemy.orm import Session, joinedload,selectinload
from app.models.organizations import Organization,OrganizationPhone, organization_activity
from app.models.activity import Activity
from app.models.building import Building
from app.schemas.organizations import OrganizationCreate
from sqlalchemy import func

"""
Модуль CRUD-операций для работы с организациями.

Содержит функции создания, получения и поиска организаций
по различным критериям: по зданию, деятельности, координатам и т.д.
"""

def create_organization(db: Session, org_in: OrganizationCreate):
    """
        Создаёт новую организацию в базе данных.

        1. Добавляет запись об организации с указанным зданием.
        2. Привязывает телефоны к организации.
        3. Привязывает виды деятельности (если указаны ID).
    """
    org = Organization(
        name=org_in.name,
        building_id=org_in.building_id,
    )
    # Телефоны
    for phone in org_in.phones:
        org.phones.append(OrganizationPhone(phone=phone.phone))
    # Деятельность
    if org_in.activity_ids:
        activities = db.query(Activity).filter(Activity.id.in_(org_in.activity_ids)).all()
        org.activities.extend(activities)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

def get_organizations(db: Session):
    """
        Возвращает список всех организаций из базы данных.
    """
    return db.query(Organization).all()

def get_organizations_by_building(db:Session,building_id:int):
    """
        Возвращает все организации, находящиеся в указанном здании.
    """
    return db.query(Organization).filter(Organization.building_id == building_id).all()

def get_organizations_by_name_activites(db:Session,activity_name:str):
    """
        Возвращает все организации, которые занимаются указанным видом деятельности.
    """
    return db.query(Organization).join(Organization.activities).filter(Activity.name == activity_name).all()

def get_organizations_by_coordinates(db:Session,latitude:float,longitude:float):
    """
        Возвращает все организации, находящиеся в здании по заданным координатам.
    """
    return db.query(Organization).join(Organization.building).filter(Building.latitude == latitude and Building.longitude == longitude).all()

def get_organization_by_id(db: Session,organization_id:int):
    """
        Возвращает одну организацию по её идентификатору.
    """
    return db.query(Organization).filter(Organization.id == organization_id).first()

def get_organization_by_name(db: Session,organization_name:str):
    return db.query(Organization).filter(Organization.name == organization_name).first()


def get_organizations_by_activity_name(db: Session, activity_name: str):
    """
        Возвращает все организации, связанные с указанной деятельностью,
        включая родительские и дочерние виды.

        Логика:
        1. Находит активность по названию (без учёта регистра).
        2. Рекурсивно собирает все связанные ID — родителей и потомков.
        3. Возвращает все организации, у которых есть эти виды деятельности.
    """
    activity = db.query(Activity).filter(func.lower(Activity.name) == activity_name.lower()).first()
    if not activity:
        return []

    # рекурсивный сбор id всех детей
    def collect_children(act):
        ids = [act.id]
        for child in getattr(act, "children", []):
            ids.extend(collect_children(child))
        return ids

    # рекурсивный сбор id всех родителей
    def collect_parents(act):
        if getattr(act, "parent", None):
            return [act.parent.id] + collect_parents(act.parent)
        return []

    ids = set(collect_children(activity) + collect_parents(activity))

    return (
        db.query(Organization)
        .join(Organization.activities)
        .filter(Activity.id.in_(ids))
        .all()
    )
