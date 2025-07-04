from sqlalchemy import delete, text, Float, select
from database.db import async_session, create_tables
from collections import defaultdict
from cobra.io import load_json_model
from model.PathwayModel import PathwayModel
from model.ReactionModel import ReactionModel, MetaboliteReactionLink, PathwayReactionLink
from model.MetaboliteModel import MetaboliteModel
from database.grouped_pathways import GROUPED_PATHWAYS
from database.objective_options import OBJECTIVE_OPTIONS
import os
def get_model_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, '..', 'database', 'iJO1366.json')
async def seed():
    async with async_session() as session:
        
        model_path = get_model_path()
        model = load_json_model(model_path)
        for entry in GROUPED_PATHWAYS:
            
            result = await session.execute(
                select(PathwayModel).where(PathwayModel.name == entry["name"])
            )
            existing = result.scalar_one_or_none()
            if existing is None:
                existing = PathwayModel(name=entry["name"], category = entry["category"]) 
                session.add(existing)

            for obj in OBJECTIVE_OPTIONS:
                if entry["name"] in obj["suggestedPathways"]:
                    existing.objective = obj["label"]

            await session.flush()  

            for rxn in model.reactions:
                if entry["name"] in rxn.subsystem:
                    result = await session.execute(
                        select(ReactionModel).where(ReactionModel.name == rxn.name)
                    )
                    reaction = result.scalar_one_or_none()
                    if not reaction:
                        reaction = ReactionModel(entry_id = rxn.id, name = rxn.name,  equation=str(rxn.reaction), subsystem = rxn.subsystem, 
                        lowerbound = rxn.lower_bound, upperbound = rxn.upper_bound)
                        session.add(reaction)
                        await session.flush() 
                        link = PathwayReactionLink(
                            pathway_id=existing.id,
                            reaction_id=reaction.id
                        )
                        session.add(link)
                        for met, coeff in rxn.metabolites.items():
                            result = await session.execute(select(MetaboliteModel).where(MetaboliteModel.name == met.id))
                            
                            metabolite = result.scalar_one_or_none()
                            if not metabolite:
                                metabolite = MetaboliteModel(name = met.id)
                                session.add(metabolite)
                                await session.flush()
                            link = MetaboliteReactionLink(reaction_id = reaction.id, metabolite_id = metabolite.id, coeff = coeff)

                            session.add(link)

                            await session.commit()


