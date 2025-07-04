from cobra.io import load_json_model
from cobra.flux_analysis import pfba
from database.db import async_session
from typing import List, Optional
from model.FluxModel import FluxModel
from model.ReactionModel import FluxReactionLink
from type.type import FluxType, FluxReactionLinkType
from strawberry.types import Info
from resolver.reaction_resolver import get_reaction_by_entry_id
import os
def get_model_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, '..', 'database', 'iJO1366.json')
async def run_fba(info: Info, entry_id: str) -> List[FluxType]:
    
    model_path = get_model_path()
    model = load_json_model(model_path)
    rxn_id = entry_id

    model.objective = rxn_id

    solution = pfba(model)
    fluxInputs : List[FluxType] =  []
    async with async_session() as session:
        for entry_id, flux_value in solution.fluxes.items():
            
            reaction = await get_reaction_by_entry_id(info, entry_id)
            if reaction is None:
                continue
            reactionId = reaction.id
            flux_model = FluxModel(value=flux_value)
            session.add(flux_model)
            await session.flush() 

            link_model = FluxReactionLink(
                flux_id=flux_model.id,
                reaction_id=reaction.id
            )
            session.add(link_model)

        
            flux_type = FluxType(
                id=flux_model.id,
                value=flux_model.value,
                flux_links=[
                    FluxReactionLinkType(
                        flux_id=flux_model.id,
                        reaction_id=reaction.id
                    )
                ]
            )
            fluxInputs.append(flux_type)

        await session.commit()

    return fluxInputs


