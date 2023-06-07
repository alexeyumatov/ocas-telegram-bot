# start cmd + registration

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.database.db import start_db, update_username, update_currency, get_username
from src.keyboards.registration_keyboard import reg_kb, currency_kb
from src.keyboards.menu_keyboards import main_menu_kb
from src.filters.registration_filters import NameInputCheck, CurrencyInputCheck


router = Router()
flags = {"long_operation": "typing"}


class Registration(StatesGroup):
    name_input = State()
    currency_input = State()


@router.message(Command("start"), flags=flags)
async def start_cmd(message: Message):
    await start_db(message.from_user.id)
    await message.answer(text="<b>Добро пожаловать!</b>\nЯ бот, который может переводить валюты",
                         reply_markup=reg_kb)


@router.callback_query(Text("registration", ignore_case=True))
async def registration_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text="Введите ваше имя (не более 60 символов):",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=None)
    await state.set_state(Registration.name_input)
    await callback.answer()


@router.message(Registration.name_input, F.text, NameInputCheck(), flags=flags)
async def name_input(message: Message, state: FSMContext):
    await message.answer(text=f"Отлично, <b>{message.text}</b>!\n\n"
                         "Теперь введите или выберите предпочитаемую валюту для перевода (ее можно будет сменить в настройках)\n"
                         "Примеры формата ввода: <i>RUB</i>, <i>USD</i>, <i>EUR</i>\n\n"
                         "Коды можно просмотреть "
                         '<a href="https://www.geostat.ge/media/20898/9-Currency-Classification-ISO-4217-2015.pdf">здесь</a>',
                         reply_markup=currency_kb)
    await update_username(message.from_user.id, message.text)
    await state.set_state(Registration.currency_input)


@router.message(Registration.name_input, flags=flags)
async def wrong_name_input(message: Message):
    await message.answer(text="Ввод имени некоректен! Попробуйте еще раз.")


@router.message(Registration.currency_input, F.text, CurrencyInputCheck(), flags=flags)
async def currency_input(message: Message, state: FSMContext):
    await message.answer(text=f"Валюта по умолчанию успешно добавлена!\n\nЗдравствуйте, <b>{await get_username(message.from_user.id)}</b>!",
                         reply_markup=main_menu_kb)
    await state.clear()
    await update_currency(message.from_user.id, message.text.upper())


@router.callback_query(Registration.currency_input, Text(startswith="curr_", ignore_case=True))
async def currency_input_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    currency = callback.data.split("_")[1]
    await bot.edit_message_text(text="Валюта по умолчанию успешно добавлена!\n\n"
                                f"Здравствуйте, <b>{await get_username(callback.from_user.id)}</b>!\nВы в главном меню.",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=main_menu_kb)
    await update_currency(callback.from_user.id, currency)
    await state.clear()
    await callback.answer()


@router.message(Registration.currency_input)
async def wrong_currency_input(message: Message):
    await message.answer(text="Ввод валюты некоректен! Попробуйте еще раз.")
