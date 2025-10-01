from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.cats import Base


if TYPE_CHECKING:
    from src.models.missions import Mission


class Target(Base):
    __tablename__ = 'targets'
    __table_args__ = (UniqueConstraint('mission_id', 'name', name='uq_target_mission_name'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    mission_id: Mapped[int] = mapped_column(Integer, ForeignKey('missions.id', ondelete='CASCADE'), nullable=False)

    # relationship
    mission: Mapped['Mission'] = relationship(back_populates='targets')
