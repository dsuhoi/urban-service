import hashlib
from enum import Enum as PyEnum

import sqlalchemy as sa

from .databases import Base


def generate_token(user_id: int) -> str:
    token = hashlib.sha256(str(user_id).encode()).hexdigest()
    return token


class SubscriptionType(PyEnum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)
    token = sa.Column(sa.String(64), nullable=False, unique=True)
    _subscription_type = sa.Column(
        "subscription_type",
        sa.Enum(SubscriptionType),
        nullable=False,
        default=SubscriptionType.FREE,
    )
    available_requests = sa.Column(sa.Integer, nullable=False, default=0)

    @property
    def subscription_type(self) -> str:
        return self._subscription_type.value

    @subscription_type.setter
    def subscription_type(self, value: str | SubscriptionType):
        if isinstance(value, str):
            # Конвертируем строку в объект Enum
            self._subscription_type = SubscriptionType(value)
        elif isinstance(value, SubscriptionType):
            self._subscription_type = value
        else:
            raise ValueError(f"Invalid subscription type: {value}")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', token='{self.token}')>"
