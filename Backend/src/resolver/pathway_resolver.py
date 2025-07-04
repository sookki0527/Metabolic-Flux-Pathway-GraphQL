from typing import List, Optional

import strawberry
from database.db import get_db, async_session
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload
from type.type import PathwayType, PathwayReactionLinkType
from model.PathwayModel import PathwayModel
from strawberry.types import Info

async def get_pathways(info) -> List[PathwayType]:
    async with async_session() as session:
        result = await session.execute(
            select(PathwayModel).options(
                selectinload(PathwayModel.pathway_links)
            )
        )
        pathways = result.scalars().all()
        return [
            PathwayType(
                id=p.id,
                name=p.name,
                category = p.category,
                objective = p.objective,
                pathway_links=[
                    PathwayReactionLinkType(
                        pathway_id=pl.pathway_id,
                        reaction_id=pl.reaction_id
                    )
                    for pl in p.pathway_links
                ]
            )
            for p in pathways
        ]


async def get_pathway(info, pathway_id: int) -> Optional[PathwayType]:
    async with async_session() as session:
        result = await session.execute(
            select(PathwayModel).options(
                selectinload(PathwayModel.pathway_links)
            ).where(PathwayModel.id == pathway_id)
        )
        pathway = result.scalar_one_or_none()
        if not pathway:
            return None

        return PathwayType(
            id=pathway.id,
            name=pathway.name,
            category = pathway.category,
            objective = pathway.objective,
            pathway_links=[
                PathwayReactionLinkType(
                    pathway_id=pl.pathway_id,
                    reaction_id=pl.reaction_id
                )
                for pl in pathway.pathway_links
            ]
        )

async def get_pathways_by_category(info, category: str) -> List[PathwayType]:
    async with async_session() as session:
        result = await session.execute(
            select(PathwayModel).options(
                selectinload(PathwayModel.pathway_links)
            ).where(PathwayModel.category == category)
        )
        pathways = result.scalars().all()
        return [
            PathwayType(
                id=p.id,
                name=p.name,
                category = p.category,
                objective = p.objective,
                pathway_links=[
                    PathwayReactionLinkType(
                        pathway_id=pl.pathway_id,
                        reaction_id=pl.reaction_id
                    )
                    for pl in p.pathway_links
                ]
            )
            for p in pathways
        ]


async def get_pathways_by_objective(info, objective: str) -> List[PathwayType]:
    async with async_session() as session:
        result = await session.execute(
            select(PathwayModel).options(
                selectinload(PathwayModel.pathway_links)
            ).where(PathwayModel.objective == objective)
        )
        pathways = result.scalars().all()
        return [
            PathwayType(
                id=p.id,
                name=p.name,
                category = p.category,
                objective = p.objective,
                pathway_links=[
                    PathwayReactionLinkType(
                        pathway_id=pl.pathway_id,
                        reaction_id=pl.reaction_id
                    )
                    for pl in p.pathway_links
                ]
            )
            for p in pathways
        ]