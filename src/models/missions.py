from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.cats import Base, SpyCat
from src.models.targets import Target


if TYPE_CHECKING:
    from src.models.cats import SpyCat
    from src.models.targets import Target


class Mission(Base):
    __tablename__ = 'missions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # FK to SpyCat (nullable until assigned)
    cat_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('spy_cats.id', ondelete='SET NULL'),
        nullable=True,
    )

    # relationships
    cat: Mapped[Optional['SpyCat']] = relationship(back_populates='missions')
    targets: Mapped[list['Target']] = relationship(back_populates='mission', cascade='all, delete-orphan')
