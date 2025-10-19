from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

"""
Модель базы данных для видов деятельности организаций.

Поддерживает иерархическую структуру (до 3 уровней вложенности).
"""

class Activity(Base):
    """
        Модель вида деятельности.

        Используется для классификации организаций по видам деятельности.
        Может образовывать древовидную структуру через parent/children.
    """
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=True)
    level = Column(Integer, nullable=False, default=1)

    # Связи
    parent = relationship("Activity", remote_side=[id], backref="children", doc="Родительская деятельность")
    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities",
        doc="Организации, связанные с данным видом деятельности"
    )