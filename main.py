import os
import asyncio

from aiogram import Bot, Dispatcher

from src.middlewares.chat_action import ChatActionMiddleware
from src.handlers import start_handler, settings_handler


async def main():
    bot = Bot(token=os.environ.get("TOKEN"), parse_mode="HTML")
    dp = Dispatcher()
    
    dp.message.middleware(middleware=ChatActionMiddleware())

    dp.include_router(start_handler.router)
    dp.include_router(settings_handler.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
