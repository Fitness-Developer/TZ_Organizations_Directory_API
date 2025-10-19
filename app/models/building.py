from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

"""
Модель базы данных для зданий, в которых располагаются организации.
"""

class Building(Base):
    """
        Модель здания.

        Хранит информацию об адресе и географических координатах.
        С одним зданием может быть связано несколько организаций.
    """
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Связь с организациями
    organizations = relationship("Organization", back_populates="building", doc="Организации, расположенные в этом здании")