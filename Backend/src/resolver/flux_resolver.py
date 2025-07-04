from typing import List, Optional

import strawberry
from database.db import get_db, async_session
from sqlalchemy import delete, insert, select
from sqlalchemy.orm import selectinload

from strawberry.types import Info
from type.type import FluxReactionLinkType, FluxType
from type.input import FluxInput
from model.FluxModel import FluxModel
from model.ReactionModel import FluxReactionLink

async def add_flux(info: Info, inputs: List[FluxInput]) -> List[FluxType]:
    async with async_session() as session:
        results = []
        for fluxInput in inputs:
          
            result = await session.execute(
                select(FluxReactionLink)
                .options(selectinload(FluxReactionLink.flux))
                .where(FluxReactionLink.reaction_id == fluxInput.reaction_id)
            )
            existing_link = result.scalar_one_or_none()

            if existing_link:
             
                existing_link.flux.value = fluxInput.value
                await session.flush()
                await session.refresh(existing_link.flux)

                results.append(
                    FluxType(
                        id=existing_link.flux.id,
                        value=existing_link.flux.value,
                        flux_links=[
                            FluxReactionLinkType(
                                flux_id=existing_link.flux_id,
                                reaction_id=existing_link.reaction_id
                            )
                        ]
                    )
                )
            else:
               
                new_flux = FluxModel(value=fluxInput.value)
                link = FluxReactionLink(reaction_id=fluxInput.reaction_id)
                new_flux.flux_links = [link]
                session.add(new_flux)

                await session.flush()
                await session.refresh(new_flux)

                results.append(
                    FluxType(
                        id=new_flux.id,
                        value=new_flux.value,
                        flux_links=[
                            FluxReactionLinkType(
                                flux_id=link.flux_id,
                                reaction_id=link.reaction_id,
                            )
                        ]
                    )
                )

        await session.commit()
        return results
