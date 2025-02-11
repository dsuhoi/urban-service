from langchain_core.messages import HumanMessage
from langchain_core.runnables import chain

visual_chooser_schema = {
    "title": "building-checker",
    "description": "Determines whether there is an design/architecture object (building or interior or design) in the photo and, if necessary, generates a list of tags describing a potential architecture bureau. You may also consider data from the ADD_INFO block when forming the tags (optional).",
    "type": "object",
    "properties": {
        "is_design": {
            "type": "boolean",
            "description": "true if there is an design/architectural object (building or interior or design style) in the image; otherwise false",
        },
        "description": {
            "type": ["string", "null"],
            "description": "A short description of the building or design in the photo (if is_building=false, then output null).",
        },
        "bureaus_tags": {
            "type": "array",
            "description": "A list of tags (no more than 5) characterizing the architecture bureau that can build the specified object. Populated only if is_building=true, otherwise an empty list.",
            "items": {"type": "string"},
            "maxItems": 5,
        },
    },
    "required": ["is_building", "building_description", "bureaus_tags"],
}


def generate_agent(llm):
    visual_agent = llm.with_structured_output(visual_chooser_schema)

    @chain
    async def visual_decode_agent(inputs: dict) -> dict:
        base64_image = inputs["image_bytes"]
        input_msg = [
            HumanMessage(
                content=[
                    {"type": "text", "text": f"ADD_INFO: {inputs["input"]}"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ]
            )
        ]
        result = await visual_agent.ainvoke(input_msg)
        return result

    return visual_decode_agent
