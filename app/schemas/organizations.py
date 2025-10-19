from pydantic import BaseModel
from typing import List, Optional
from app.schemas.building import BuildingOut
from app.schemas.activity import ActivityOut

"""
Схемы (Pydantic) для работы с организациями, их телефонами, зданиями и деятельностью.

Используются для валидации входных данных и сериализации ответов API.
"""

# -------------------------------------------------------------------
# Телефоны организации
# -------------------------------------------------------------------
class PhoneBase(BaseModel):
    """Базовая схема телефонного номера организации."""
    phone: str

class PhoneCreate(PhoneBase):
    pass

class PhoneOut(PhoneBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

# -------------------------------------------------------------------
# Организации
# -------------------------------------------------------------------
class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    """
       Схема для создания новой организации.

       Содержит:
       - building_id — ID здания, в котором находится организация;
       - phones — список телефонов организации;
       - activity_ids — список ID видов деятельности.
    """
    building_id: int
    phones: List[PhoneCreate] = []
    activity_ids: List[int] = []

class OrganizationOut(OrganizationBase):
    """
    Схема для отображения информации об организации в ответе API.

    Включает:
    - building — данные о здании, где находится организация;
    - phones — список телефонов;
    - activities — список видов деятельности.
    """
    id: int
    building: Optional[BuildingOut]
    phones: List[PhoneOut] = []
    activities: List[ActivityOut] = []

    model_config = {
        "from_attributes": True
    }