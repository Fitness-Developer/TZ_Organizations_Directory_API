from pydantic import BaseModel
from typing import Optional

"""
Схемы (Pydantic) для работы со зданиями.

Содержат информацию об адресе и координатах.
"""


class BuildingBase(BaseModel):
    """Базовая схема здания."""
    address: str
    latitude: float
    longitude: float

class BuildingCreate(BuildingBase):
    pass

class BuildingOut(BuildingBase):
    id: int

    model_config = {
        "from_attributes": True
    }