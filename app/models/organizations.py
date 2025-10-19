from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

"""
Модели базы данных для Организаций и связанных сущностей.
"""

# Ассоциативная таблица "многие ко многим" между Организациями и Деятельностями
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)

class Organization(Base):
    """
    Модель организации.

    Представляет карточку организации в справочнике.
    Организация связана:
      - с одним зданием (`building`)
      - с несколькими телефонами (`phones`)
      - с несколькими видами деятельности (`activities`)
    """
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="SET NULL"))

    # Связи
    building = relationship("Building", back_populates="organizations")
    phones = relationship(
        "OrganizationPhone",
        cascade="all, delete-orphan",
        back_populates="organization",
        doc="Список телефонов организации"
    )
    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations",
        doc="Виды деятельности, которыми занимается организация"
    )

class OrganizationPhone(Base):
    """
    Модель телефонных номеров организации.

    Каждая запись соответствует одному телефону конкретной организации.
    """
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(50), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))

    # Обратная связь
    organization = relationship("Organization", back_populates="phones")