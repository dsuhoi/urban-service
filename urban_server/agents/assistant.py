from langchain_core.prompts import ChatPromptTemplate

assistant_schemas = {
    "title": "assistant",
    "description": """Ассистент, который предоставляет информацию о проекте Urban Service.
Является профессиональным менеджером по коммуникациям в сфере урбанистики. Должен либо вывести информацию,
запрашиваемую у пользователя INPUT блока, которая относится ТОЛЬКО к теме урбанистики или данного сервиса, либо переадресовать запрос на агента-урбаниста (urban), если в запросе присутствует явная просьба в помощи поиска арх. бюро по описанию арх. объекта!""",
    "type": "object",
    "properties": {
        "agent_type": {
            "description": "Тип ответа. `simple` - ответ на вопрос пользователя о сервисе, `urban` - переадресация на агента-урбаниста",
            "type": "string",
            "enum": ["simple", "urban"],
        },
        "response": {
            "description": "Финальный ответ на вопрос пользователя в `simple` режиме. Иначе вернуть null! На запросы пользователя ЖЕЛАТЕЛЬНО отвечать 1-3 предложениями! Если запрос не относится к урбанистике или арх. объекту, то напиши вежливый отказ от запроса в одно предложение",
            "type": ["string", "null"],
        },
    },
}

help_prompt = """Urban Service
Данный сервис предназначен для помощи в выборе архитектурного бюро на основе ваших запросов.
Вам лишь достаточно подробно описать ваш объект и желаемые критерии арх. бюро для реализации этого объекта.
Чем подробнее будет описание, тем лучше получится подобрать арх. бюро под ваши запросы.
"""

prompt = ChatPromptTemplate.from_messages(
    [("user", "INPUT: {input}"), ("assistant", "HELP:\n{help_prompt}")]
)


def prepare_help_prompt(input_prompt):
    return help_prompt if input_prompt and (input_prompt != "") else input_prompt


def generate_agent(llm):
    return (
        {
            "input": lambda x: x["input"],
            "help_prompt": lambda x: prepare_help_prompt(["help_prompt"]),
        }
        | prompt
        | llm.with_structured_output(assistant_schemas)
    )
