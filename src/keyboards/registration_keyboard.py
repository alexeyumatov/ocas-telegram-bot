from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


reg_btn = [[InlineKeyboardButton(
    text="🧑‍💻 Зарегестрироваться", callback_data="registration")]]

reg_kb = InlineKeyboardMarkup(inline_keyboard=reg_btn)


currency_btns = [[InlineKeyboardButton(text="💸 Популярные валюты", callback_data='no_action')],
                 [InlineKeyboardButton(text="🇺🇸 Доллары", callback_data="curr_USD"),
                  InlineKeyboardButton(text="🇪🇺 Евро", callback_data="curr_EUR"),
                  InlineKeyboardButton(text="🇷🇺 Рубли", callback_data="curr_RUB")],
                  [InlineKeyboardButton(text="🇰🇿 Тенге", callback_data="curr_KZT"),
                   InlineKeyboardButton(text="🇬🇧 Фунты", callback_data="curr_GBP"),
                   InlineKeyboardButton(text="🇨🇳 Юани", callback_data="curr_CNY")],
                   [InlineKeyboardButton(text="🇺🇦 Гривни", callback_data="curr_UAH"),
                    InlineKeyboardButton(text="🇧🇾 Бел. рубль", callback_data="curr_BYN")]]

currency_kb = InlineKeyboardMarkup(inline_keyboard=currency_btns)
