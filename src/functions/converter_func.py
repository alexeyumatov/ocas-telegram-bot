import aiohttp

from src.database.db import get_currency


async def convert(user_id, to):
    saved_currency = await get_currency(user_id)
    headers = {
        "apikey": "FsMd8HgHdkvTHoRXL4aBWZTN55SbLNEi"
    }
    params = {"to": to, "from": saved_currency, "amount": 1}
    url = f"https://api.apilayer.com/currency_data/convert"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers, ssl=False) as resp:
            result = await resp.json()
    if result["success"] == True:
        return round(result["result"], 2)
    return "error"
