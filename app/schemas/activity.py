from pydantic import BaseModel
from typing import Optional, List, ForwardRef

"""
Схемы (Pydantic) для видов деятельности организаций.

Поддерживают древовидную структуру с вложенностью до 3 уровней.
"""

class ActivityBase(BaseModel):
    """Базовая схема вида деятельности."""
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    """Схема для создания нового вида деятельности."""
    pass

ActivityOut = ForwardRef("ActivityOut")

class ActivityOut(BaseModel):
    """
        Схема для отображения вида деятельности в ответе API.

        Позволяет отображать дерево вложенных активностей (через поле `children`).
    """
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int
    children: List["ActivityOut"] = []

    model_config = {
        "from_attributes": True
    }

# Разрешаем рекурсивную ссылку на саму себя
ActivityOut.update_forward_refs()