import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from resolver.reaction_resolver import get_reaction_by_id
from type.type import FluxType, PathSegment
from typing import List
from strawberry.types import Info
async def build_flux_graph(info: Info, fluxes: List[FluxType]) -> nx.DiGraph:
    G = nx.DiGraph()

    for flux in fluxes:
        for link in flux.flux_links:
            reaction = await get_reaction_by_id(info, link.reaction_id)  
            
            substrates = [ml.metabolite_id for ml in reaction.metabolite_links if ml.coeff < 0]
            products = [ml.metabolite_id for ml in reaction.metabolite_links if ml.coeff > 0]

            for s in substrates:
                for p in products:
                    G.add_edge(s, p, weight=abs(flux.value), reaction_id=reaction.id)

    return G

async def dijkstra(info: Info, G: nx.DiGraph, metabolite_A_id:int, metabolite_B_id : int) -> List[PathSegment]:
        
    shortest_path = nx.dijkstra_path(G, source=metabolite_A_id, target=metabolite_B_id, weight='weight')
    pathsegments = []
    for u, v in zip(shortest_path, shortest_path[1:]):
        edge = G.get_edge_data(u, v)
        reaction_id = edge['reaction_id']
        reaction = await get_reaction_by_id(info, reaction_id)
        path = PathSegment(from_ = u, to_ = v, reaction_id = reaction_id, reaction_name = reaction.name)
        pathsegments.append(path)
        
    return pathsegments