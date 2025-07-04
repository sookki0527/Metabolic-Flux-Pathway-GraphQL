from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column
from typing import List
from database.db import Base
class MetaboliteModel(Base):
    __tablename__ = "metabolites"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    metabolite_links: Mapped[List["MetaboliteReactionLink"]] = relationship(back_populates="metabolite")
    