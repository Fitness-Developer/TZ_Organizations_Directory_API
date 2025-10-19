from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.activity import ActivityCreate, ActivityOut
from app.crud.activity import create_activity, get_activities, build_activity_tree

router = APIRouter(prefix="/activities", tags=["Activities"])

# -------------------------------------------------------------------------
# Создание нового вида деятельности
# -------------------------------------------------------------------------
@router.post(
    "/",
    response_model=ActivityOut,
    summary="Создать вид деятельности",
    description="""
Создает новый вид деятельности.  
Если указан `parent_id`, проверяет существование родителя и уровень вложенности (максимум 3).
"""
)
def create_activity_endpoint(activity_in: ActivityCreate, db: Session = Depends(get_db)):
    try:
        activity = create_activity(db, activity_in)
        return build_activity_tree(activity)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании деятельности: {str(e)}"
        )

# -------------------------------------------------------------------------
# Получить список всех видов деятельности (в виде дерева)
# -------------------------------------------------------------------------
@router.get(
    "/",
    response_model=List[ActivityOut],
    summary="Получить все виды деятельности",
    description="""
Возвращает иерархический список всех видов деятельности (в виде дерева).  
Родительские виды находятся на верхнем уровне, дочерние — внутри.
"""
)
def get_all_activities(db: Session = Depends(get_db)):
    activities = get_activities(db)
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Виды деятельности не найдены"
        )
    return activities