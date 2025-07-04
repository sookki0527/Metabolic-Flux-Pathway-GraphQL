from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Float
from database.db import Base
from typing import List

class FluxModel(Base):
    __tablename__ = "flux"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[float]
    flux_links: Mapped[List["FluxReactionLink"]] = relationship(back_populates="flux")


