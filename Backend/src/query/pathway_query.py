import strawberry
from typing import List, Optional
from type.type import PathwayType
from strawberry.types import Info
from resolver.pathway_resolver import get_pathway, get_pathways, get_pathways_by_category, get_pathways_by_objective


@strawberry.type
class PathwayQuery:
    @strawberry.field
    async def pathways(self, info: Info) -> List[PathwayType]:
        pathways = await get_pathways(info)
        return pathways

    @strawberry.field
    async def pathway(self, info: Info, pathway_id: int) -> PathwayType:
        pathway = await get_pathway(info, pathway_id)
        return pathway

    @strawberry.field
    async def pathway_by_category(self, info: Info, category: str) -> List[PathwayType]:
        pathways = await get_pathways_by_category(info, category)
        return pathways
    
    @strawberry.field
    async def pathways_by_objective(self, info: Info, objective: str) -> List[PathwayType]:
        pathways = await get_pathways_by_objective(info, objective)
        return pathways

