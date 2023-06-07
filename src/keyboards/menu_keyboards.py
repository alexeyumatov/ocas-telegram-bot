from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main_menu_bttns = [
    [InlineKeyboardButton(text="💱 Конвертер валют", callback_data="converter")],
    [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")]
]

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=main_menu_bttns)


settings_bttns = [
    [InlineKeyboardButton(text="✏️ Изменить имя", callback_data="name_change"),
     InlineKeyboardButton(text="✏️ Изменить валюту", callback_data="currency_change")],
     [InlineKeyboardButton(text="⬅️ Вернуться в главное меню", callback_data="back_to_menu")]
]


settings_kb = InlineKeyboardMarkup(inline_keyboard=settings_bttns)
