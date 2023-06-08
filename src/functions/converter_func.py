import aiohttp

from src.database.db import get_currency


async def convert(user_id, from_curr):
    saved_currency = await get_currency(user_id)
    headers = {
        "apikey": "FsMd8HgHdkvTHoRXL4aBWZTN55SbLNEi"
    }
    params = {"to": saved_currency, "from": from_curr, "amount": 1}
    url = f"https://api.apilayer.com/currency_data/convert"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers, ssl=False) as resp:
            result = await resp.json()
    if result["success"] == True:
        return round(result["result"], 2)
    return "error"
