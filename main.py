import os
import asyncio

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.middlewares.chat_action import ChatActionMiddleware
from src.handlers import start_handler, settings_handler, converter_handler
from src.database.db import clear_number_of_requests
from src.handlers.scheduled_tasks import clear_requests


async def main():
    bot = Bot(token=os.environ.get("TOKEN"), parse_mode="HTML")
    dp = Dispatcher()
    
    dp.message.middleware(middleware=ChatActionMiddleware())

    dp.include_router(start_handler.router)
    dp.include_router(settings_handler.router)
    dp.include_router(converter_handler.router)
    
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(clear_requests, trigger='interval', seconds=600)
    scheduler.start()
    
    await clear_number_of_requests()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
