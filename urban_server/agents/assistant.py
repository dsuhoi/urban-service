from langchain_core.prompts import ChatPromptTemplate

assistant_schemas = {
    "title": "assistant",
    "description": "An assistant providing information about the Urban Service project. Serves as a professional communications manager in the field of urbanism. It should either respond to the user's inquiry within the INPUT block, only if it's related to urbanism or this service, or redirect the query to the urban agent if there is a clear request for assistance in finding architectural bureaus based on a description of an architectural object.",
    "type": "object",
    "properties": {
        "agent_type": {
            "description": "Type of response. `support` - answer the user's question about the service/assistant or urban themes, `urban` - redirect to the urban agent for findnig arch. bureaus, `others` - all other questions not related to service/assistant/urban.",
            "type": "string",
            "enum": ["support", "urban", "others"],
        },
        "response": {
            "description": "The final response to the user's question in `support` mode. Otherwise, return null. Ideally, respond to the user's queries in 1-3 sentences. If the query is unrelated to urbanism or architectural objects, politely decline the request in a single sentence.",
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
