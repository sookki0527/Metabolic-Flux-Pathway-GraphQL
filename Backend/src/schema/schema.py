from __future__ import annotations
import typing
import strawberry
from strawberry.types import Info

from query.pathway_query import PathwayQuery
from query.reaction_query import ReactionQuery
from mutation.flux_mutation import FluxMutation
from mutation.network_mutation import NetworkMutation
@strawberry.type
class Query(PathwayQuery, ReactionQuery):
    pass

@strawberry.type 
class Mutation(FluxMutation, NetworkMutation):
    pass