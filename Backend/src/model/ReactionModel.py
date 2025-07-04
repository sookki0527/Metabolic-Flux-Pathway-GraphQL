from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Float, String
from database.db import Base
from typing import List, Optional
class ReactionModel(Base):
    __tablename__ = "reactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entry_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(unique = True)
    equation: Mapped[str]
    subsystem: Mapped[str]
    lowerbound: Mapped[int]
    upperbound: Mapped[int]
    metabolite_links: Mapped[List["MetaboliteReactionLink"]] = relationship(back_populates="reaction")
    pathway_links: Mapped[List["PathwayReactionLink"]] = relationship(back_populates="reaction")
    flux_links: Mapped[List["FluxReactionLink"]] = relationship(back_populates="reaction")



class MetaboliteReactionLink(Base):
    __tablename__ = "metabolite_reaction"
    reaction_id = mapped_column(ForeignKey("reactions.id"), primary_key=True)
    metabolite_id = mapped_column(ForeignKey("metabolites.id"), primary_key=True)
    coeff = mapped_column(Float)  
    
    reaction = relationship("ReactionModel", back_populates="metabolite_links")
    metabolite = relationship("MetaboliteModel", back_populates = "metabolite_links")


class PathwayReactionLink(Base):
    __tablename__ = "pathway_reaction"
    pathway_id = mapped_column(ForeignKey("pathways.id"), primary_key=True)
    reaction_id = mapped_column(ForeignKey("reactions.id"), primary_key=True)
  
    pathway = relationship("PathwayModel", back_populates="pathway_links")
    reaction = relationship("ReactionModel", back_populates="pathway_links")


class FluxReactionLink(Base):
    __tablename__ = "flux_reaction"
    flux_id = mapped_column(ForeignKey("flux.id"), primary_key=True)
    reaction_id = mapped_column(ForeignKey("reactions.id"), primary_key=True)
  
    flux = relationship("FluxModel", back_populates="flux_links")
    reaction = relationship("ReactionModel", back_populates="flux_links")