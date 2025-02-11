import base64
import json

import core.schemas as schemas
from agents.assistant import generate_agent as generate_assistant_agent
from agents.urban_agent import generate_agent as generate_urban_agent
from agents.visual_agent import generate_agent as generate_visual_agent
from core.auth import User, get_available_user
from core.llm import llm
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

router = APIRouter(prefix="/assistant")

urban_llm = generate_urban_agent(llm)
assistant_llm = generate_assistant_agent(llm)
visual_agent = generate_visual_agent(llm)


@router.post("/", response_model=schemas.AssistentResponse)
async def assistant(
    input_data: schemas.InputUrban, user: User = Depends(get_available_user)
):
    response = await assistant_llm.ainvoke(
        {"input": input_data.input, "help_prompt": input_data.help_prompt}
    )
    if response["agent_type"] == "urban":
        result = await urban_llm.ainvoke({"input": input_data.input})
    elif response["agent_type"] == "support":
        result = response["response"]
    else:
        result = None

    return {"agent_type": response["agent_type"], "response": result}


@router.post("/visual", response_model=schemas.AssistentVisualResponse)
async def visual_assistant(
    input_data: str = Form(...),
    file: UploadFile = File(...),
    user: User = Depends(get_available_user),
):
    try:
        input_data = schemas.VisualUrbanInput(**json.loads(input_data))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    image_bytes = base64.b64encode(await file.read()).decode("utf-8")

    response = await visual_agent.ainvoke(
        {"input": input_data.input, "image_bytes": image_bytes}
    )
    return {
        "is_building": response["is_building"],
        "building_description": response["building_description"],
        "tags": response["bureaus_tags"],
    }
