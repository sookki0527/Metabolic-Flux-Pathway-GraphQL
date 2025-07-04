import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from fastapi.middleware.cors import CORSMiddleware
from schema.schema import Query, Mutation
from database.seed import seed
from database.db import Base, engine, create_tables, delete_tables, async_session
from sqlalchemy import select
from model.ReactionModel import ReactionModel
import asyncio
schema = strawberry.Schema(query=Query, mutation = Mutation)

graphql_app = GraphQLRouter(schema)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(graphql_app, prefix="/graphql-apple")


@app.on_event("startup")
async def on_startup():
    await delete_tables()
    await create_tables()
    await seed()
  
