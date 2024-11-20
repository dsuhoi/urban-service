from langchain_core.prompts import ChatPromptTemplate

classifier_agent_schema = {
    "title": "classifier-bureaus",
    "description": "Описание тегов, характеризующих заданное архитектурное бюро для его идентификации по возможным тегам пользователя.",
    "type": "object",
    "properties": {
        "tags": {
            "description": "Массив из тегов (число ЗАВИСИТ от объема информации, НЕ пиши лишних тегов).",
            "type": "array",
            "items": {
                "description": "Тег, который должен быть не более 1-3 слов, которые было бы удобно перевести в эмбеддинги.\
НЕ пиши очевидные теги [архиктура, градостроительство и т.п.], старайся выделить те, что могут отличать это бюро от других [НЕ пиши в тегах о наградах или конкретных проектах]",
                "type": "string",
            },
            "minItems": 1,
            "maxItems": 5,
        },
    },
    "required": ["tags"],
}


writer_agent_schema = {
    "title": "writer-bureau",
    "description": "Выбрать лучшее арх. бюро из блока BUREAUS, которое соответствует запросу пользователя в INPUT.\
Детально описать это лучшее бюро в отчете.",
    "type": "object",
    "properties": {
        "name": {"description": "Название лучшего бюро.", "type": "string"},
        "descr": {
            "description": "Краткое описание бюро и информация о том, как оно поможет пользователю с его запросом.",
            "type": "string",
        },
        # "projects": {
        #     "description": "Описание релевантных для пользователя проектов бюро. Если их нет, то ВСЕГДА выводи NULL.",
        #     "type": ["string", "null"],
        # },
    },
    "required": ["name", "descr"],
}

prompt_writer = ChatPromptTemplate.from_messages(
    [("user", "INPUT: {input}"), ("assistant", "BUREAUS: {bureaus}")]
)


def prepare_bureaus(bureaus):
    return "\n---\n".join(
        [
            f"Name: {b['name']}\nYear and Country: {b['year']}, {b['country']}\nDescription: {b['description']}\nProjects: {b['projects']}\nAwards: {b['awards']}"
            for b in bureaus
        ]
    )


def generate_writer_agent(llm):
    return (
        {"input": lambda x: x["input"], "bureaus": lambda x: x["bureaus"]}
        | prompt_writer
        | llm.with_structured_output(writer_agent_schema)
    )


def generate_tags_agent(llm):
    return llm.with_structured_output(classifier_agent_schema)
