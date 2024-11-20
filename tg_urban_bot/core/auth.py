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


async def free_bonus(user_id: int, password: str | None = None):
    password = "urban_bonus" if password is None else password
    resp = await aioreq._request(
        "/users/bonus_by_token",
        method="POST",
        json={"password": password},
        auth=tg_auth_cred(user_id),
    )
    if resp.status == 200:
        return "Вам доступно ещё 10 бесплатных запросов!"
    else:
        return "Пароль неверный!"
