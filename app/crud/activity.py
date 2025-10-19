from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate

"""
Модуль CRUD-операций для работы с видами деятельности.

Содержит функции создания видов деятельности, построения дерева вложенности
и получения всех активностей в иерархической структуре.
"""

def create_activity(db: Session, activity_in: ActivityCreate, level: int = 1):
    """
    Создаёт новый вид деятельности.

    Если указан parent_id, то вычисляет уровень вложенности
    относительно родителя и проверяет, что он не превышает 3.

    Args:
        db (Session): активная сессия SQLAlchemy
        activity_in (ActivityCreate): входные данные для создания активности
        level (int, optional): уровень вложенности. По умолчанию — 1.

    Raises:
        ValueError: если родительская активность не найдена
        ValueError: если уровень вложенности больше 3

    Returns:
        Activity: созданная запись о виде деятельности
    """
    if activity_in.parent_id:
        parent = db.query(Activity).filter(Activity.id == activity_in.parent_id).first()
        if not parent:
            raise ValueError(f"Родитель с id={activity_in.parent_id} не найден")
        level = parent.level + 1
        if level > 3:
            raise ValueError("Уровень вложенности не может превышать 3")
    activity = Activity(name=activity_in.name, parent_id=activity_in.parent_id, level=level)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity

def build_activity_tree(activity: Activity):
    """
    Рекурсивно строит дерево вида деятельности, включая все дочерние элементы.

    Args:
        activity (Activity): экземпляр активности

    Returns:
        dict: словарь с данными активности и её дочерних элементов
    """
    return {
        "id": activity.id,
        "name": activity.name,
        "parent_id": activity.parent_id,
        "level": activity.level,
        "children": [build_activity_tree(child) for child in activity.children]
    }

def get_activities(db: Session):
    """
        Возвращает все виды деятельности в виде дерева (иерархической структуры).

        Находит все корневые активности (у которых parent_id == None)
        и рекурсивно строит их потомков.

        Returns:
            List[dict]: дерево всех видов деятельности
        """
    roots = db.query(Activity).filter(Activity.parent_id == None).all()
    return [build_activity_tree(act) for act in roots]