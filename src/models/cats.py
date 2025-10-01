from typing import TYPE_CHECKING

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from src.models.missions import Mission


class Base(DeclarativeBase):
    pass


# -------- Spy Cat --------
class SpyCat(Base):
    __tablename__ = 'spy_cats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    breed: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    # one-to-many: one cat can have multiple missions, but only one active at a time
    missions: Mapped[list['Mission']] = relationship(back_populates='cat', cascade='all, delete-orphan')
