from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.config import currencies_list


class NameInputCheck(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if len(message.text) > 60:
            return False
        else:
            return True


class CurrencyInputCheck(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text.upper() in currencies_list:
            return True
        return False
