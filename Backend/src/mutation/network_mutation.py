import strawberry
from database.db import async_session
from resolver.flux_resolver import add_flux
from cobra_py.fba import run_fba
from type.type import FluxType, PathSegment
from type.input import FluxResultInput
from resolver.reaction_resolver import get_reaction_by_entry_id, get_reaction_by_id
from resolver.metabolite_resolver import get_metabolite_byname
from typing import List, Optional
from strawberry.types import Info
from network.network import build_flux_graph, dijkstra
@strawberry.type
class NetworkMutation:
    @strawberry.field
    async def networkResult(self, info: Info, result: FluxResultInput, source_metabolite: str) -> List[PathSegment]:
        async with async_session() as session:

            fluxes = result.fluxes
            G = await build_flux_graph(fluxes)
            reaction_id = result.objective_flux_reactionId
            reaction = await get_reaction_by_id(info, reaction_id)
            products = [ml.metabolite_id for ml in reaction.metabolite_links if ml.coeff > 0]
            metabolite = await get_metabolite_byname(source_metabolite)
            return await dijkstra(G, metabolite.id, products[-1])
