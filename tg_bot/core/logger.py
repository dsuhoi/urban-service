import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler
from aiogram import types

class AsyncLogger:
    def __init__(self, name="bot_logger", log_file="bot.log", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    async def info(self, message: str):
        await self._log_async(logging.INFO, message)

    async def error(self, message: str):
        await self._log_async(logging.ERROR, message)

    async def _log_async(self, level: int, message: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._sync_log, level, message)

    def _sync_log(self, level: int, message: str):
        self.logger.log(level, message)


def setup_logger():
    return AsyncLogger()


class ExceptionLoggingMiddleware:
    def __init__(self, logger: AsyncLogger | None = None):
        super().__init__()
        self.logger = logger if logger else setup_logger()

    async def __call__(self, handler, event: types.Message, data: dict):
        username = event.from_user.username if event.from_user else "unknown"
        message_text = event.text
        id_ = event.message_id

        await self.logger.info(f"INPUT | ID: {id_},\t User: {username},\t Request: {message_text}")

        try:
            return await handler(event, data)
        except Exception as e:
            await self.logger.error(f"ID: {id_} # {e}")
            raise
