from langchain_core.prompts import ChatPromptTemplate

urban_chooser_json_schema = {
    "title": "urban-chooser",
    "description": "Fill out the form based on the input request related to urbanism to select the best architectural bureau. Use ONLY the information provided by the user (if insufficient information is available, return null for the respective parameters).",
    "type": "object",
    "properties": {
        "project_title": {
            "description": "The title of the project (no more than 4-5 words) based on the user's request.",
            "type": "string",
        },
        "base_params": {
            "description": "Key parameters of the project.",
            "type": "object",
            "properties": {
                "function": {
                    "description": "The function of the object.",
                    "type": ["string", "null"],
                    "enum": [
                        "Жилье",
                        "Офисы",
                        "Коммерция / торговля",
                        "Многофункциональные комплексы",
                        "ТПУ и инфраструктурные объекты",
                        "Образование",
                        "Здравоохранение",
                        "Спортивные объекты",
                        "Культурные объекты",
                        "Временная архитектура и арт-объекты",
                        "Редевелопмент",
                        "Благоустройство",
                        "Интерьеры",
                        "Мастер-план застройки",
                    ],
                },
                "area": {
                    "description": "The area of the object (m²).",
                    "type": ["number", "null"],
                    "minimum": 1.0,
                },
            },
            "required": ["function", "area"],
        },
        "criteria": {
            "description": "Selection criteria for the architectural bureau based on the user's project requirements.",
            "type": "object",
            "properties": {
                "experience": {
                    "description": "Required experience of the bureau: established firms (10+ years on the market), young names (less than 10 years), specific project experience (if specific expertise is needed).",
                    "type": ["string", "null"],
                    "enum": [
                        "Опытные бюро",
                        "Молодые имена",
                        "Опыт реализации проектов",
                        "Не важен",
                    ],
                },
                "altitude": {
                    "description": "Specialization of the bureau by building height (150m+, 50-150m, or under 50m).",
                    "type": ["string", "null"],
                    "enum": ["High", "Medium", "Low"],
                },
                "tags": {
                    "description": "Tags characterizing the bureau for the project.",
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 3,
                    "maxItems": 5,
                },
            },
            "required": ["experience", "altitude", "tags"],
        },
        "correction": {
            "description": "Used when there are null parameters or criteria and is intended for additional questions to the user.",
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
