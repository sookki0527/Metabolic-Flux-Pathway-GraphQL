from __future__ import annotations
import strawberry
from typing import List, Optional
from database.db import async_session
from sqlalchemy import select
from model.MetaboliteModel import MetaboliteModel
from model.ReactionModel import ReactionModel
from model.PathwayModel import PathwayModel
from model.FluxModel import FluxModel
@strawberry.type
class MetaboliteReactionLinkType:
    reaction_id: int
    metabolite_id: int
    coeff: float
    @strawberry.field
    async def metabolite(self, info: Info) -> Optional[MetaboliteType]:
        async with async_session() as session:
            result = await session.execute(
                select(MetaboliteModel).where(MetaboliteModel.id == self.metabolite_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return MetaboliteType(id=m.id, name=m.name)

@strawberry.type
class PathwayReactionLinkType:
    pathway_id: int
    reaction_id: int
    @strawberry.field
    async def reaction(self, info: Info) -> Optional[ReactionType]:
        async with async_session() as session:
            result = await session.execute(
                select(ReactionModel).where(ReactionModel.id == self.reaction_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return ReactionType(id=m.id, name=m.name, equation = m.equation, subsystem = m.subsystem, lowerbound = m.lowerbound, upperbound = m.upperbound)
    @strawberry.field
    async def pathway(self, info: Info) -> Optional[PathwayType]:
            async with async_session() as session:
                result = await session.execute(
                    select(PathwayModel).where(PathwayModel.id == self.pathway_id)
                )
                m = result.scalar_one_or_none()
                if not m:
                    return None
                return PathwayType(id=m.id, name=m.name, category = m.category, objective = m.objective)
@strawberry.type
class FluxReactionLinkType:
    flux_id: int
    reaction_id: int
    @strawberry.field
    async def flux(self, info: Info) -> Optional[FluxType]:
        async with async_session() as session:
            result = await session.execute(
                select(FluxModel).where(FluxModel.id == self.flux_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return FluxType(id=m.id, value=m.value)

    @strawberry.field
    async def reaction(self, info: Info) -> Optional[ReactionType]:
        async with async_session() as session:
            result = await session.execute(
                select(ReactionModel).where(ReactionModel.id == self.reaction_id)
            )
            m = result.scalar_one_or_none()
            if not m:
                return None
            return ReactionType(id=m.id, entry_id = m.entry_id, name=m.name, subsystem = m.subsystem, equation = m.equation, lowerbound = m.lowerbound, upperbound = m.upperbound)


@strawberry.type
class ReactionType:
    id: int
    entry_id: Optional[str] = None
    name: str
    equation: str
    subsystem: str
    lowerbound: int
    upperbound: int
    metabolite_links: Optional[List[MetaboliteReactionLinkType]] = None
    pathway_links: Optional[List[PathwayReactionLinkType]] = None
    flux_links: Optional[List[FluxReactionLinkType]] = None

    

@strawberry.type
class MetaboliteType:
    id: int
    name: str
    metabolite_links: Optional[List["MetaboliteReactionLinkType"]] = None


@strawberry.type
class PathwayType:
    id: int
    name: str
    category:str
    objective: Optional[str]
    pathway_links: Optional[List["PathwayReactionLinkType"]] = None

@strawberry.type
class FluxType:
    id: int
    value: float
    flux_links: Optional[List["FluxReactionLinkType"]] = None


@strawberry.type
class FluxResultType:
    objective_flux_reactionId : Optional[int]
    objective_flux_value: Optional[float]
    top_fluxes: List[FluxType]
    total_flux: float
    non_zero_flux_count: int
    fluxes: List[FluxType]
    candidate_source_metabolites : List[str]
    source_metabolite : Optional[str]
    segments: List[PathSegment]



@strawberry.type
class PathSegment:
    from_: int
    to_: int
    reaction_id: int
    reaction_name: str
