from src.database.db import clear_number_of_requests


async def clear_requests():
    await clear_number_of_requests()
