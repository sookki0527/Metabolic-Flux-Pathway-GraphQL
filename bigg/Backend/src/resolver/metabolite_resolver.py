from typing import List, Optional

import strawberry
from database.db import get_db, async_session
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload
from model.MetaboliteModel import MetaboliteModel
from model.ReactionModel import MetaboliteReactionLink
from strawberry.types import Info
from type.type import MetaboliteType, MetaboliteReactionLinkType
async def get_metabolites(info) -> List[MetaboliteType]:
    async with async_session() as session:
        result = await session.execute(
            select(MetaboliteModel).options(
                selectinload(MetaboliteModel.metabolite_links)
            )
        )
        metabolites = result.scalars().all()
        return [
            MetaboliteType(
                id=m.id,
                name=m.name,
                metabolite_links=[
                    MetaboliteReactionLinkType(
                        metabolite_id=ml.metabolite_id,
                        reaction_id=ml.reaction_id
                    )
                    for ml in m.metabolite_links
                ]
            )
            for m in metabolites
        ]


async def get_metabolite(info, metabolite_id: int) -> Optional[MetaboliteType]:
    async with async_session() as session:
        result = await session.execute(
            select(MetaboliteModel).options(
                selectinload(MetaboliteModel.metabolite_links)  
            ).where(MetaboliteModel.id == metabolite_id)
        )
        metabolite = result.scalar_one_or_none()
        if not metabolite:
            return None

        return MetaboliteType(
            id=metabolite.id,
            name=metabolite.name,
            metabolite_links=[
                MetaboliteReactionLinkType(
                    metabolite_id=ml.metabolite_id,
                    reaction_id=ml.reaction_id,
                    coeff=ml.coeff 
                )
                for ml in metabolite.metabolite_links
            ]
        )
async def get_metabolite_byname(info: Info, name : str) -> Optional[MetaboliteType]:
     async with async_session() as session:
        result = await session.execute(
            select(MetaboliteModel).options(
                selectinload(MetaboliteModel.metabolite_links) 
            ).where(MetaboliteModel.name == name)
        )
        metabolite = result.scalar_one_or_none()
        if not metabolite:
            return None

        return MetaboliteType(
            id=metabolite.id,
            name=metabolite.name,
            metabolite_links=[
                MetaboliteReactionLinkType(
                    metabolite_id=ml.metabolite_id,
                    reaction_id=ml.reaction_id,
                    coeff=ml.coeff  # coeff 필드가 있다면 포함
                )
                for ml in metabolite.metabolite_links
            ]
        )