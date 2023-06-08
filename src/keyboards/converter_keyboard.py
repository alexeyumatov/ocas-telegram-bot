from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.database.db import get_last_used_currency, get_currency


async def make_keyboard(user_id) -> InlineKeyboardMarkup:
    currency_btns = [[InlineKeyboardButton(text="💸 Предложенные валюты", callback_data='no_action')],
                     [InlineKeyboardButton(text="🇺🇸 Доллары", callback_data="curr_USD"),
                      InlineKeyboardButton(
                      text="🇪🇺 Евро", callback_data="curr_EUR"),
                      InlineKeyboardButton(text="🇷🇺 Рубли", callback_data="curr_RUB")],
                     [InlineKeyboardButton(text="🇰🇿 Тенге", callback_data="curr_KZT"),
                      InlineKeyboardButton(
                         text="🇬🇧 Фунты", callback_data="curr_GBP"),
                      InlineKeyboardButton(text="🇨🇳 Юани", callback_data="curr_CNY")],
                     [InlineKeyboardButton(text="🇺🇦 Гривни", callback_data="curr_UAH"),
                      InlineKeyboardButton(text="🇧🇾 Бел. рубль", callback_data="curr_BYN")],
                     [InlineKeyboardButton(
                         text="⌨️ Ввести вручную", callback_data="curr_byhand"),
                     InlineKeyboardButton(text="⏪ В главное меню", callback_data="back_to_menu")]]
    last_used_currency = await get_last_used_currency(user_id)
    if last_used_currency == None:
        return InlineKeyboardMarkup(inline_keyboard=currency_btns)
    else:
        currency_btns.insert(4, [InlineKeyboardButton(text="🙋 Последняя выбранная валюта", callback_data='no_action')])
        currency_btns.insert(5, [InlineKeyboardButton(text=f"{await get_currency(user_id)} -> {last_used_currency}", callback_data='last_used')])
        return InlineKeyboardMarkup(inline_keyboard=currency_btns)


convert_bttns = [[InlineKeyboardButton(text="✏️ Сменить валюту по умолчанию", callback_data="currency_change")],
                 [InlineKeyboardButton(
                     text="✏️ Выбрать другую валюту", callback_data="converter")],
                 [InlineKeyboardButton(text="⏪ В главное меню", callback_data="back_to_menu")]]

convert_kb = InlineKeyboardMarkup(inline_keyboard=convert_bttns)


server_error_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text="⏪ В главное меню", callback_data="back_to_menu")]])
