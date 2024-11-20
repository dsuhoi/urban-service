from langchain_core.prompts import ChatPromptTemplate

urban_chooser_json_schema = {
    "title": "urban-chooser",
    "description": "Заполнить форму на основе входного запроса на тему урбанистики для выбора лучшего арх. бюро. \
Используй ТОЛЬКО информацию от пользователя (если нет достаточной информации, то выводи null по параметрам)!",
    "type": "object",
    "properties": {
        "project_title": {
            "description": "Название проекта (не более 4-5 слов) на основе запроса пользователя",
            "type": "string",
        },
        "base_params": {
            "description": "Основные параметры проекта.",
            "type": "object",
            "properties": {
                "function": {
                    "description": "Функции объекта.",
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
                    "description": "Площадь объекта (м^2).",
                    "type": ["number", "null"],
                    "minimum": 1.0,
                },
            },
            "required": ["function", "area"],
        },
        "criteria": {
            "description": "Критерии выбора арх. бюро на основе пожелания пользователя по проекту!",
            "type": "object",
            "properties": {
                "experience": {
                    "description": "Необходимый опыт бюро. Опытные бюро (от 10 лет на рынке), \
                    молодые имена (до 10 лет), опыт реализации проектов (если требуется опыт в конкретной области архитектуры).",
                    "type": ["string", "null"],
                    "enum": [
                        "Опытные бюро",
                        "Молодые имена",
                        "Опыт реализации проектов",
                        "Не важен",
                    ],
                },
                "altitude": {
                    "description": "Специализация бюро по высотности зданий (150м, 50-150м или до 50м).",
                    "type": ["string", "null"],
                    "enum": ["Высокие", "Средние", "Низкие"],
                },
                "tags": {
                    "description": "Теги, которые могут характеризовать бюро для проекта.",
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "minItems": 3,
                    "maxItems": 5,
                },
            },
            "required": ["experience", "altitude", "tags"],
        },
        "correction": {
            "description": "Используется при наличие null параметров или критериев и направлен на доп. вопросы к пользователю",
            "type": ["array", "null"],
            "items": {
                "description": "Вопрос к пользователю для заполнения неизвестного (null) параметра или критерия (ОБЯЗАТЕЛЬНО).",
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
