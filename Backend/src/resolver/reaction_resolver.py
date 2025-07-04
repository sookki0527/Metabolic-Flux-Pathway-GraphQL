from typing import List, Optional

import strawberry
from database.db import get_db, async_session
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload
from type.type import ReactionType, MetaboliteReactionLinkType, PathwayReactionLinkType, FluxReactionLinkType
from model.ReactionModel import ReactionModel, PathwayReactionLink

from strawberry.types import Info

async def get_reactions(info)-> List[ReactionType]:
    async with async_session() as session:
        result = await session.execute(select(ReactionModel).options(
            selectinload(ReactionModel.metabolite_links),
            selectinload(ReactionModel.pathway_links),
            selectinload(ReactionModel.flux_links)))
        reactions = result.scalars().all()   
        return [
                ReactionType(
                    id = r.id,
                    entry_id = r.entry_id,
                    name = r.name,
                    equation = r.equation,
                    subsystem = r.subsystem,
                    lowerbound = r.lowerbound,
                    upperbound = r.upperbound,
                    metabolite_links=[
                        MetaboliteReactionLinkType(
                            reaction_id=mr.reaction_id,
                            metabolite_id=mr.metabolite_id,
                            coeff=mr.coeff,
                        )
                    for mr in r.metabolite_links
                    ],
                    pathway_links=[
                        PathwayReactionLinkType(
                            pathway_id=pr.pathway_id,
                            reaction_id=pr.reaction_id,
                        )
                        for pr in r.pathway_links
                    ],
                    flux_links = [
                            FluxReactionLinkType(
                                flux_id = fr.flux_id,
                                reaction_id = fr.reaction_id
                            )
                            for fr in r.flux_links
                    ]
                
            )
            for r in reactions
        ]


async def get_reactions_by_pathway(info: Info, pathway_id : int) -> List[ReactionType]:
    async with async_session() as session:
        result = await session.execute(select(ReactionModel)
        .options(
            selectinload(ReactionModel.metabolite_links),
            selectinload(ReactionModel.pathway_links),
            selectinload(ReactionModel.flux_links)
            )
        #.where(ReactionModel.subsystem.ilike(f"%{pathway}%"))
         .join(ReactionModel.pathway_links)
        .where(PathwayReactionLink.pathway_id == pathway_id)
        )
        reactions = result.scalars().all()   
        return [
            ReactionType(
                    id = r.id,
                    entry_id = r.entry_id,
                    name = r.name,
                    equation = r.equation,
                    subsystem = r.subsystem,
                    lowerbound = r.lowerbound,
                    upperbound = r.upperbound,
                    metabolite_links=[
                    MetaboliteReactionLinkType(
                        reaction_id=mr.reaction_id,
                        metabolite_id=mr.metabolite_id,
                        coeff=mr.coeff,
                    )
                    for mr in r.metabolite_links
                ],
                pathway_links=[
                    PathwayReactionLinkType(
                        pathway_id=pr.pathway_id,
                        reaction_id=pr.reaction_id,
                    )
                    for pr in r.pathway_links
                ],
                flux_links = [
                        FluxReactionLinkType(
                            flux_id = fr.flux_id,
                            reaction_id = fr.reaction_id
                        )
                        for fr in r.flux_links
                    ]
            )
            for r in reactions
        ]

async def get_reaction_by_entry_id(info: Info, entry_id: str) -> Optional[ReactionType]:   
    async with async_session() as session:
        result = await session.execute(select(ReactionModel)
        .options(
            selectinload(ReactionModel.metabolite_links),
            selectinload(ReactionModel.pathway_links),
            selectinload(ReactionModel.flux_links)
            )
        #.where(ReactionModel.subsystem.ilike(f"%{pathway}%"))
        .where(ReactionModel.entry_id == entry_id)
        )
        r = result.scalar_one_or_none()  
        if r is None:
            return None
        return ReactionType(
                    id = r.id,
                    entry_id = r.entry_id,
                    name = r.name,
                    equation = r.equation,
                    subsystem = r.subsystem,
                    lowerbound = r.lowerbound,
                    upperbound = r.upperbound,
                    metabolite_links=[
                        MetaboliteReactionLinkType(
                            reaction_id=mr.reaction_id,
                            metabolite_id=mr.metabolite_id,
                            coeff=mr.coeff,
                        )
                    for mr in r.metabolite_links
                    ],
                    pathway_links=[
                        PathwayReactionLinkType(
                            pathway_id=pr.pathway_id,
                            reaction_id=pr.reaction_id,
                        )
                        for pr in r.pathway_links
                    ],
                    flux_links = [
                        FluxReactionLinkType(
                            flux_id = fr.flux_id,
                            reaction_id = fr.reaction_id
                        )
                        for fr in r.flux_links
                    ]
            )

async def get_reaction_by_id(info: Info, reaction_id: int) -> Optional[ReactionType]:   
    async with async_session() as session:
        result = await session.execute(select(ReactionModel)
        .options(
            selectinload(ReactionModel.metabolite_links),
            selectinload(ReactionModel.pathway_links),
            selectinload(ReactionModel.flux_links)
            )
        #.where(ReactionModel.subsystem.ilike(f"%{pathway}%"))
        .where(ReactionModel.id == reaction_id)
        )
        r = result.scalar_one_or_none()  
        if r is None:
            return None
        return ReactionType(
                    id = r.id,
                    entry_id = r.entry_id,
                    name = r.name,
                    equation = r.equation,
                    subsystem = r.subsystem,
                    lowerbound = r.lowerbound,
                    upperbound = r.upperbound,
                    metabolite_links=[
                        MetaboliteReactionLinkType(
                            reaction_id=mr.reaction_id,
                            metabolite_id=mr.metabolite_id,
                            coeff=mr.coeff,
                        )
                    for mr in r.metabolite_links
                    ],
                    pathway_links=[
                        PathwayReactionLinkType(
                            pathway_id=pr.pathway_id,
                            reaction_id=pr.reaction_id,
                        )
                        for pr in r.pathway_links
                    ],
                    flux_links = [
                        FluxReactionLinkType(
                            flux_id = fr.flux_id,
                            reaction_id = fr.reaction_id
                        )
                        for fr in r.flux_links
                    ]
            )
        