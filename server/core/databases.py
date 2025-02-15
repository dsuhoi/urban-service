import json
import os
from pathlib import Path
from typing import AsyncGenerator

import chromadb
import numpy as np
from chromadb import AsyncHttpClient
from chromadb.config import Settings
from chromadb.types import Collection
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.llm import embeddings

engine = create_async_engine(os.getenv("USER_DATABASE_URL"))
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


chroma_client: AsyncHttpClient = None
bureau_collection: Collection = None


async def get_chroma_client() -> AsyncHttpClient:
    global chroma_client
    if chroma_client is None:
        chroma_client = await chromadb.AsyncHttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=os.getenv("CHROMA_PORT", 8000),
            settings=Settings(
                anonymized_telemetry=False,
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_client_auth_credentials=os.getenv(
                    "CHROMA_SERVER_AUTH_CREDENTIALS"
                ),
            ),
        )
    return chroma_client


async def get_bureau_collection() -> Collection:
    global bureau_collection
    chroma_client = await get_chroma_client()
    if bureau_collection is None:
        bureau_collection = await chroma_client.get_collection(name="architect_bureaus")
    return bureau_collection


async def init_chromadb():
    chroma_client: AsyncHttpClient = await get_chroma_client()
    collection = await chroma_client.get_or_create_collection(name="architect_bureaus")
    if (await collection.count()) == 0:
        raise Exception("Empty database")


async def get_relevant_bureau(tags: list[str], res_count: int = 3) -> dict:
    collection = await get_bureau_collection()

    query_emb = np.mean(await embeddings.aembed_documents(tags), axis=0)

    bureaus = await collection.query(query_embeddings=[query_emb], n_results=res_count)
    return bureaus["metadatas"][0]
