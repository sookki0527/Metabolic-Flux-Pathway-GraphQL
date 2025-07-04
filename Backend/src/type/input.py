from __future__ import annotations
import strawberry
from typing import List, Optional
from database.db import async_session
from sqlalchemy import select
from model.MetaboliteModel import MetaboliteModel
from model.ReactionModel import ReactionModel
from model.PathwayModel import PathwayModel
from model.FluxModel import FluxModel
@strawberry.input
class MetaboliteReactionLinkInput:
    reaction_id: int
    metabolite_id: int
    coeff: float
    @strawberry.field
    async def metabolite(self, info: Info) -> Optional[MetaboliteInput]:
        async with async_session() as session:
            result = await session.execute(
                select(MetaboliteModel).where(MetaboliteModel.id == self.metabolite_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return MetaboliteInput(id=m.id, name=m.name)

@strawberry.input
class PathwayReactionLinkInput:
    pathway_id: int
    reaction_id: int
    @strawberry.field
    async def reaction(self, info: Info) -> Optional[ReactionInput]:
        async with async_session() as session:
            result = await session.execute(
                select(ReactionModel).where(ReactionModel.id == self.reaction_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return ReactionInput(id=m.id, name=m.name, equation = m.equation, subsystem = m.subsystem, lowerbound = m.lowerbound, upperbound = m.upperbound)
    @strawberry.field
    async def pathway(self, info: Info) -> Optional[PathwayInput]:
            async with async_session() as session:
                result = await session.execute(
                    select(PathwayModel).where(PathwayModel.id == self.pathway_id)
                )
                m = result.scalar_one_or_none()
                if not m:
                    return None
                return PathwayInput(id=m.id, name=m.name, category = m.category, objective = m.objective)
@strawberry.input
class FluxReactionLinkInput:
    flux_id: int
    reaction_id: int
    @strawberry.field
    async def flux(self, info: Info) -> Optional[FluxInput]:
        async with async_session() as session:
            result = await session.execute(
                select(FluxModel).where(FluxModel.id == self.flux_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return FluxInput(id=m.id, value=m.value)

    @strawberry.field
    async def reaction(self, info: Info) -> Optional[ReactionInput]:
        async with async_session() as session:
            result = await session.execute(
                select(ReactionModel).where(ReactionModel.id == self.reaction_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return ReactionInput(id=m.id, entry_id = m.entry_id, name=m.name, subsystem = m.subsystem, equation = m.equation, lowerbound = m.lowerbound, upperbound = m.upperbound)


@strawberry.input
class ReactionInput:
    id: int
    entry_id: Optional[str] = None
    name: str
    equation: str
    subsystem: str
    lowerbound: int
    upperbound: int
    metabolite_links: Optional[List[MetaboliteReactionLinkInput]] = None
    pathway_links: Optional[List[PathwayReactionLinkInput]] = None
    flux_links: Optional[List[FluxReactionLinkInput]] = None

    

@strawberry.input
class MetaboliteInput:
    id: int
    name: str
    metabolite_links: Optional[List["MetaboliteReactionLinkInput"]] = None


@strawberry.input
class PathwayInput:
    id: int
    name: str
    category:str
    objective: Optional[str]
    pathway_links: Optional[List["PathwayReactionLinkInput"]] = None

@strawberry.input
class FluxInput:
    id: int
    value: float
    flux_links: Optional[List["FluxReactionLinkInput"]] = None


@strawberry.input
class FluxResultInput:
    objective_flux_reaction_id : Optional[int]
    objective_flux_value: Optional[float]
    top_fluxes: List[FluxInput]
    total_flux: float
    non_zero_flux_count: int
    fluxes: List[FluxInput]
    candidate_source_metabolites : List[str]



@strawberry.input
class PathSegment:
    from_: int
    to_: int
    reaction_id: int
