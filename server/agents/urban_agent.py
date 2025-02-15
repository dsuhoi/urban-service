from langchain_core.prompts import ChatPromptTemplate

urban_chooser_json_schema = {
    "title": "urban-chooser",
    "description": "Fill out the form based on the input request related to urbanism to select the best architectural bureau. Use ONLY the information provided by the user (if insufficient information is available, return null for the respective parameters).",
    "type": "object",
    "properties": {
        "project_title": {
            "description": "The title of the project (no more than 4-5 words) based on the user's request",
            "type": "string",
        },
        "base_params": {
            "description": "Key parameters of the project",
            "type": "object",
            "properties": {
                "function": {
                    "description": "The function class of the object (like home, office, garden, etc.)",
                    "type": ["string", "null"],
                },
                "tags": {
                    "description": "Useful tags that characterize an object",
                    "type": "array",
                    "items": {
                        "description": "Tag in the form of 1-2 words",
                        "type": "string"
                    },
                    "maxItems": 4
                }
            },
            "required": ["function", "tags"],
        },
        "criteria": {
            "description": "Selection criteria for the architectural bureau based on the user's project requirements.",
            "type": "object",
            "properties": {
                "experience": {
                    "description": "Required experience of the bureau: established firms (10+ years on the market), young names (less than 10 years), specific project experience (if specific expertise is needed).",
                    "type": ["string", "null"],
                    "enum": [
                        "Great experience",
                        "Little experience",
                        "Not important",
                    ],
                },
                "tags": {
                    "description": "Useful and important tags characterizing the bureau for the project/object.",
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 5,
                },
            },
            "required": ["experience", "altitude", "tags"],
        },
        "correction": {
            "description": "Used when there are null parameters or criteria and is intended for additional questions to the user. If the user feels confident in the input request, then always return null!",
            "type": ["array", "null"],
            "items": {
                "description": "A question for the user to fill in an unknown (null) parameter or criterion (MANDATORY).",
                "type": "string",
            },
        },
    },
    "required": ["project_title", "base_params", "criteria", "correction"],
}
prompt = ChatPromptTemplate.from_messages([("user", "INPUT: {input}")])


def generate_agent(llm):
    return (
        {"input": lambda x: x["input"]}
        | prompt
        | llm.with_structured_output(urban_chooser_json_schema)
    )
