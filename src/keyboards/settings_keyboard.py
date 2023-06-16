from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


currency_btns = [[InlineKeyboardButton(text="💸 Предложенные валюты", callback_data='no_action')],
                 [InlineKeyboardButton(text="🇺🇸 Доллары", callback_data="curr_USD"),
                  InlineKeyboardButton(text="🇪🇺 Евро", callback_data="curr_EUR"),
                  InlineKeyboardButton(text="🇷🇺 Рубли", callback_data="curr_RUB")],
                  [InlineKeyboardButton(text="🇰🇿 Тенге", callback_data="curr_KZT"),
                   InlineKeyboardButton(text="🇬🇧 Фунты", callback_data="curr_GBP"),
                   InlineKeyboardButton(text="🇨🇳 Юани", callback_data="curr_CNY")],
                   [InlineKeyboardButton(text="🇺🇦 Гривни", callback_data="curr_UAH"),
                    InlineKeyboardButton(text="🇧🇾 Бел. рубль", callback_data="curr_BYN")],
                   [InlineKeyboardButton(text="⌨️ Ввести вручную", callback_data="curr_byhand")],
                   [InlineKeyboardButton(text="⏪ В меню настроек", callback_data="back_to_settings")]]

currency_kb = InlineKeyboardMarkup(inline_keyboard=currency_btns)

stop_action_btns = [[InlineKeyboardButton(text="⏪ Отменить действие", callback_data="back_to_settings")]]

stop_action_kb = InlineKeyboardMarkup(inline_keyboard=stop_action_btns)
