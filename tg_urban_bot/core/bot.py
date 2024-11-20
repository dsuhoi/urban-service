from aiogram import Bot, Dispatcher
from config import CONFIG

bot = Bot(token=CONFIG.TG_TOKEN)
dp = Dispatcher()
