import os

from pydantic import BaseModel


class Config(BaseModel):
    SERVER_URL: str = os.getenv("SERVER_URL", "http://0.0.0.0:8001")
    TG_TOKEN: str = os.getenv("TG_TOKEN")
    PAYMENTS_TOKEN: str = os.getenv("PAYMENTS_TOKEN")


CONFIG = Config()
