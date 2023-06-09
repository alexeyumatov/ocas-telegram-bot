from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.keyboards.menu_keyboards import settings_kb, main_menu_kb
from src.keyboards.settings_keyboard import currency_kb, stop_action_kb
from src.filters.registration_filters import NameInputCheck, CurrencyInputCheck
from src.database.db import update_currency, update_username, get_username, get_currency


router = Router()
flags = {"long_operation": "typing"}


class Settings(StatesGroup):
    changing_name = State()
    changing_currency_callback = State()
    changing_currency_by_hand = State()


@router.callback_query(Text("settings", ignore_case=True))
async def settings_menu(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text="Вы в меню настроек.\n\n"
                                "<b>Ваши данные:</b>\n"
                                f"👤 Имя\t-\t{await get_username(callback.from_user.id)}\n"
                                f"💵 Валюта по умолчанию\t-\t{await get_currency(callback.from_user.id)}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=settings_kb)
    await callback.answer()


@router.callback_query(Text(endswith="_change", ignore_case=True))
async def change_data(callback: CallbackQuery, bot: Bot, state: FSMContext):
    action = callback.data.split("_")[0]
    if action == "name":
        await state.set_state(Settings.changing_name)
        await bot.edit_message_text(text="Введите ваше новое имя:",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=stop_action_kb)
    elif action == "currency":
        await state.set_state(Settings.changing_currency_callback)
        await bot.edit_message_text(text="Выберите валюту, которая будет использоваться по умолчанию:",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=currency_kb)
    await callback.answer()


@router.message(Settings.changing_name, F.text, NameInputCheck(), flags=flags)
async def name_input(message: Message, state: FSMContext):
    await update_username(message.from_user.id, message.text)
    await message.answer(text=f"Отлично, вы сменили свое имя на <b>{message.text}</b>\n\n"
                         "<b>Ваши данные:</b>\n"
                         f"👤 Имя\t-\t{await get_username(message.from_user.id)}\n"
                         f"💵 Валюта по умолчанию\t-\t{await get_currency(message.from_user.id)}", 
                         reply_markup=settings_kb)
    await state.clear()


@router.message(Settings.changing_name, flags=flags)
async def wrong_name_input(message: Message):
    await message.answer(text="Ввод имени некоректен! Попробуйте еще раз.")


@router.callback_query(Settings.changing_currency_callback, Text(startswith="curr_", ignore_case=True))
async def currency_input_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    currency = callback.data.split("_")[1]
    if currency == 'byhand':
        await bot.edit_message_text(text="Примеры формата ввода: <i>RUB</i>, <i>USD</i>, <i>EUR</i>\n\n"
                                    "Коды можно просмотреть "
                                    '<a href="https://www.geostat.ge/media/20898/9-Currency-Classification-ISO-4217-2015.pdf">здесь</a>',
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id)
        await state.set_state(Settings.changing_currency_by_hand)
        await callback.answer()
    else:
        await update_currency(callback.from_user.id, currency)
        await bot.edit_message_text(text=f"Валюта по умолчанию успешно сменена!\n\n<b>Ваши данные:</b>\n"
                                    f"👤 Имя\t-\t{await get_username(callback.from_user.id)}\n"
                                    f"💵 Валюта по умолчанию\t-\t{await get_currency(callback.from_user.id)}",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=settings_kb)
        await state.clear()
        await callback.answer()


@router.message(Settings.changing_currency_by_hand, F.text, CurrencyInputCheck(), flags=flags)
async def currency_input(message: Message, state: FSMContext):
    await update_currency(message.from_user.id, message.text.upper())
    await message.answer(text=f"Валюта по умолчанию успешно сменена!\n\n<b>Ваши данные:</b>\n"
                         f"👤 Имя\t-\t{await get_username(message.from_user.id)}\n"
                         f"💵 Валюта по умолчанию\t-\t{await get_currency(message.from_user.id)}",
                         reply_markup=settings_kb)
    await state.clear()


@router.message(Settings.changing_currency_by_hand)
async def wrong_currency_input(message: Message):
    await message.answer(text="Ввод валюты некоректен! Попробуйте еще раз.")


@router.callback_query(Text("back_to_settings", ignore_case=True))
async def settings_menu(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text="Вы в меню настроек.\n\n"
                                "<b>Ваши данные:</b>\n"
                                f"👤 Имя\t-\t{await get_username(callback.from_user.id)}\n"
                                f"💵 Валюта по умолчанию\t-\t{await get_currency(callback.from_user.id)}",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=settings_kb)
    await callback.answer()


@router.callback_query(Text("back_to_menu", ignore_case=True))
async def back_to_menu(callback: CallbackQuery, bot: Bot):
    await bot.edit_message_text(text=f"Здравствуйте, <b>{await get_username(callback.from_user.id)}</b>!\nВы в главном меню.",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=main_menu_kb)
    await callback.answer()
