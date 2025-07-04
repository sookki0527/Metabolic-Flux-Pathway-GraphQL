import strawberry
from database.db import async_session
from resolver.flux_resolver import add_flux
from cobra_py.fba import run_fba
from type.type import FluxType, FluxResultType
from type.input import FluxInput
from resolver.reaction_resolver import get_reaction_by_entry_id, get_reaction_by_id
from resolver.metabolite_resolver import get_metabolite, get_metabolite_byname
from typing import List, Optional
from strawberry.types import Info
from network.network import build_flux_graph, dijkstra
from collections import Counter

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
@strawberry.type
class FluxMutation:
    @strawberry.field
    async def fluxResult(self, info: Info, entry_id: str) -> FluxResultType:
        async with async_session() as session:
            fluxes = await run_fba(info, entry_id)
           
            reaction = await get_reaction_by_entry_id(info, entry_id)
            

            ### 1. Objective Reaction Flux Value 
            objective_flux_value = None
            if reaction and reaction.flux_links:
            
                flux_link = reaction.flux_links[-1]
                flux_type = await flux_link.flux(info) 
                
                if flux_type:  
                    objective_flux_value = flux_type.value
                objective_flux_reactionId = flux_link.reaction_id


            #### 2. Top-N Flux values
            top_fluxes = sorted(fluxes, key=lambda f: abs(f.value), reverse=True)[:10]


            #### 3. System Summary
            non_zero_flux_count = len([f for f in fluxes if abs(f.value) > 1e-6])
            total_flux = sum(abs(f.value) for f in fluxes)


            #### 4. source candidates
            used_fluxes = [f for f in fluxes if abs(f.value) > 0]
            candidate_source_metabolites = set()
            important_substrates = []
            for f in used_fluxes:
                for link in f.flux_links:
                    reaction = await get_reaction_by_id(info, link.reaction_id)
                    for ml in reaction.metabolite_links:
                        if ml.coeff < 0:  
                            metabolite = await get_metabolite(info, ml.metabolite_id)
                            candidate_source_metabolites.add(metabolite.name)
                            important_substrates.append(metabolite.name)

            
            counter = Counter(important_substrates)
            candidates =  [met for met, _ in counter.most_common(1)]
            G = await build_flux_graph(info, fluxes)
            reaction_id = objective_flux_reactionId
            products = [ml.metabolite_id for ml in reaction.metabolite_links if ml.coeff > 0]
            
            source_metabolite = candidates[-1]
            metabolite = await get_metabolite_byname(info, source_metabolite)
            segments = await dijkstra(info, G, metabolite.id, products[-1])

            return FluxResultType(
                objective_flux_reactionId = objective_flux_reactionId,
                objective_flux_value=objective_flux_value,
                top_fluxes=top_fluxes,
                total_flux=total_flux,
                non_zero_flux_count=non_zero_flux_count,
                fluxes=fluxes,
                candidate_source_metabolites = candidate_source_metabolites,
                source_metabolite = source_metabolite,
                segments = segments
            )




# async def convert_flux_type_to_input(fluxes: List[FluxType]) -> List[FluxInput]:
#     flux_inputs = []

#     for f in fluxes:
#         link_inputs = None
#         if f.flux_links:
#             link_inputs = [
#                 FluxReactionLinkInput(
#                     flux_id=link.flux_id,
#                     reaction_id=link.reaction_id
#                 )
#                 for link in f.flux_links
#             ]

#         flux_input = FluxInput(
#             id=f.id,
#             value=f.value,
#             flux_links=link_inputs
#         )

#         flux_inputs.append(flux_input)

#     return flux_inputs
