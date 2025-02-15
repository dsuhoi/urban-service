from aiohttp import BasicAuth

from core.async_requests import aioreq


def tg_auth_cred(user_id: int):
    return BasicAuth(login=str(user_id), password=str(user_id))


async def check_user(user_id: int):
    resp = await aioreq._request("/users/me", method="GET", auth=tg_auth_cred(user_id))
    if resp.status == 200:
        user_data = await resp.json(encoding="utf-8")
        return user_data
    else:
        return None


async def registration(user_id: int):
    resp = await aioreq._request(
        "/users/signup",
        method="POST",
        json={"username": str(user_id), "password": str(user_id)},
    )
    return resp.status == 201


async def status_checker(code: int, user_id: int) -> str | None:
    if code in {401, 403}:
        if code == 401:
            await registration(user_id)
            return "Ошибка регистрации устранена! Повторите запрос"
        return "У Вас закончились запросы. Оформите новые..."

    if code != 200:
        return "Запрос некорректный!"


async def free_bonus(user_id: int, password: str | None = None, count: int = 10):
    password = "urban_bonus" if password is None else password
    resp = await aioreq._request(
        "/users/bonus_by_token",
        method="POST",
        json={"password": password, "count": count},
        auth=tg_auth_cred(user_id),
    )
    if resp.status == 200:
        return f"Вам доступно ещё {count} бесплатных запросов!"
    else:
        return "Пароль неверный!"
