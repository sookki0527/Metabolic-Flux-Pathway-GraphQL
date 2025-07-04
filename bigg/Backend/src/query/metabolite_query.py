import strawberry
from typing import List, Optional
from type.type import MetaboliteType
from strawberry.types import Info
from resolver.metabolite_resolver import get_metabolite, get_metabolites


@strawberry.type
class MetaboliteQuery:
    @strawberry.field
    async def metabolites(self, info: Info) -> List[MetaboliteType]:
        metabolites = await get_metabolites(info)
        return metabolites

    @strawberry.field
    async def metabolite(self, info: Info, metabolite_id: int) -> MetaboliteType:
        metabolite = await get_metabolite(info, metabolite_id)
        return metabolite

