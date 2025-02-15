import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import BotCommand, Message

import routers.assistant as assistant
# import routers.payments as payments
from config import CONFIG
from core.auth import check_user, free_bonus, registration
from core.logger import ExceptionLoggingMiddleware
from core.utils import COMMAND_LIST, description_meta

bot = Bot(token=CONFIG.TG_TOKEN)
dp = Dispatcher()

dp.message.middleware(ExceptionLoggingMiddleware())

# dp.include_router(payments.router)
dp.include_router(assistant.router)


@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if not (await check_user(user_id)):
        await registration(user_id)
        await free_bonus(user_id)
        await message.answer(
            """Вы успешно прошли регистрацию! В качестве бонуса у вас есть +10 бесплатный запросов к ассистенту по поводу отчетов по арх. бюро."""
        )
    await message.answer(
        "Здравствуйте, Вы можете написать по любому вопросу, связанному с Вашим объектом, арх. бюро или урбанистикой"
    )


@dp.message(Command("bonus"))
@description_meta("bonus", "Укажите пароль для получения бесплатных запросов")
async def bonus_command(message: Message):
    if len(inp := message.text.split(" ")) > 1:
        password = inp[1]
        await message.answer(await free_bonus(message.from_user.id, password))
    else:
        await message.answer("Ошибка!\nВведите пароль в сообщении с командой!")


@dp.message(Command("balance"))
@description_meta("balance", "Ваш баланс и тип подписки")
async def balance_command(message: Message):
    result = await check_user(message.from_user.id)
    await message.answer(
        f"Подписка: {result['subscription']}\nКол-во запросов: {result['available_requests']}"
    )


async def set_command_desc(bot: Bot):
    commands = [BotCommand(command=k, description=v) for k, v in COMMAND_LIST.items()]
    await bot.set_my_commands(commands)
    await bot.set_my_description(
        """Здравствуйте, это Urban Service ассистент!
Я предоставляю информацию об архитектурных бюро и готов помочь Вам подобрать лучшее решение по твоему объекту.
Просто напишите мне о том, что Вы хотите!"""
    )


async def main():
    await set_command_desc(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
