import core.schemas as schemas
from agents.bureau_agents import generate_writer_agent
from core.auth import User, get_available_user
from core.databases import get_relevant_bureau, get_session
from core.llm import embeddings, llm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/report")

writer_llm = generate_writer_agent(llm)


@router.post("/", response_model=schemas.BureauResponse)
async def report(
    input_data: schemas.BureauInput,
    user: User = Depends(get_available_user),
    db: AsyncSession = Depends(get_session),
):
    bureaus = await get_relevant_bureau(input_data.tags)
    resp = await writer_llm.ainvoke({"input": input_data.input, "bureaus": bureaus})
    best_bureau = [b for b in bureaus if b["name"] == resp["name"]][0]

    result = {
        "name": resp["name"],
        "description": resp["description"],
        "cite": best_bureau["cite"],
        "add_info": {
            "year": best_bureau["year"],
            "country": best_bureau["country"],
            "projects": best_bureau["projects"],
        },
    }

    user.available_requests -= 1
    await db.commit()

    return result
