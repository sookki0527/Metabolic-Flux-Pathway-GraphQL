from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from typing import List, Optional
from database.db import Base
class PathwayModel(Base):
    __tablename__ = "pathways"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    category: Mapped[str]
    objective: Mapped[Optional[str]] = mapped_column(nullable=True)
    pathway_links: Mapped[List["PathwayReactionLink"]] = relationship(back_populates="pathway")

