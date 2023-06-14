from typing import Callable, Dict, Awaitable, Any
from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import Message

from src.database.db import get_user_state, ban_user, set_banned_time, get_banned_time


class CheckIfBanned(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if await get_user_state(event.from_user.id):
            now_time = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
            banned_time = datetime.strptime(await get_banned_time(event.from_user.id), "%H:%M")
            period = now_time - banned_time
            if abs(period.seconds) >= 600:
                await ban_user(event.from_user.id, unban=True)
                await set_banned_time(event.from_user.id, None, delete=True)
                return await handler(event, data)
            await event.answer(f"Вы заблокированы на {10 - period.seconds // 60} минут, попробуйте позже",
                               show_alert=True)
            return
        else:
            return await handler(event, data)
