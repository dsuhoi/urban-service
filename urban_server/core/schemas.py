from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field, StringConstraints


class InputUrban(BaseModel):
    input: Annotated[str, StringConstraints(min_length=8)] = Field(
        description="Описание объекта от пользователя",
        examples=["Я хочу построить дом!"],
    )
    help_prompt: Optional[str] = Field(
        default="", description="Кастомная информация об ассистенте"
    )


class BaseQuestionParams(BaseModel):
    function: str | None = Field(description="Функции объекта")
    area: float | None = Field(description="Площадь объекта")


class Criteria(BaseModel):
    experience: str | None = Field(description="Необходимый опыт арх. бюро")
    altitude: str | None = Field(description="Класс высотности здания")
    tags: list[str] = Field(description="Набор тегов, характеризующих запрос")


class UrbanQuestionResponse(BaseModel):
    project_title: str = Field(description="Название проекта")
    base_params: BaseQuestionParams = Field(description="Основные параметры объекта")
    criteria: Criteria = Field(description="Критерии для выбора бюро под объект")
    correction: list[str] | None = Field(
        description="Описание возможных пояснений к запросу"
    )


class AssistentResponse(BaseModel):
    agent_type: Literal["support", "urban", "others"] = Field(
        description="Вид ответа. `support` - простой ответ ассистента, `urban` - ответ от урбаниста."
    )
    response: UrbanQuestionResponse | str | None = Field(
        description="Ответ либо от ассистента, либо от урбаниста.", default=None
    )


class BureauInput(BaseModel):
    input: Annotated[str, StringConstraints(min_length=5)] = Field(
        description="Основной запрос пользователя"
    )
    tags: list[str] = Field(description="Полученные от запроса теги")


class BureauAddInfo(BaseModel):
    year: int | None = Field(description="Год основания бюро")
    country: str | None = Field(description="Страна бюро")
    projects: str | None = Field(description="Релевантные проекты бюро")


class BureauResponse(BaseModel):
    name: str = Field(description="Название бюро")
    description: str = Field(description="Описание бюро")
    cite: str | None = Field(description="Сайт бюро")

    add_info: BureauAddInfo = Field(description="Доп. информация о бюро")


class LoginInput(BaseModel):
    username: str = Field(description="Логин")
    password: Annotated[str, StringConstraints(min_length=5)] = Field(
        description="Пароль"
    )


class AboutUserResponse(BaseModel):
    subscription: Literal["free", "basic", "premium"] = Field(
        description="Тип подписки"
    )
    available_requests: int = Field(description="Оставшееся кол-во запросов")


class BonusInput(BaseModel):
    password: str = Field(description="Бонус для тестирования API")


class BonusResponse(BaseModel):
    content: str = Field(description="Бонус для тестирования API")
