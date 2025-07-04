import strawberry
from typing import List, Optional
from type.type import ReactionType
from strawberry.types import Info
from resolver.reaction_resolver import get_reactions_by_pathway, get_reactions, get_reaction_by_entry_id, get_reaction_by_id


@strawberry.type
class ReactionQuery:
    @strawberry.field
    async def reactions(self, info: Info) -> List[ReactionType]:
        reactions = await get_reactions(info)
        return reactions

    @strawberry.field
    async def reactions_by_pathway(self, info: Info, pathway_id: int) -> List[ReactionType]:
        reactions = await get_reactions_by_pathway(info, pathway_id)
        return reactions


    @strawberry.field
    async def reaction_by_entry_id(self, info: Info, entry_id: str) -> ReactionType:
        reaction = await get_reaction_by_entry_id(info, entry_id)
        return reaction

    @strawberry.field
    async def reaction_by_id(self, info: Info, reaction_id : int) -> Optional[ReactionType]:
        reaction = await get_reaction_by_id(info, reaction_id)
        return reaction