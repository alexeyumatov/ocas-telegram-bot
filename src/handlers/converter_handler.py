from aiogram import Router, Bot, F
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.database.db import get_currency, update_last_used_currency, get_last_used_currency
from src.keyboards.converter_keyboard import make_keyboard, convert_kb, server_error_kb
from src.functions.converter_func import convert
from src.filters.registration_filters import CurrencyInputCheck


router = Router()
flags = {"long_operation": "typing"}


class CurrencyChoice(StatesGroup):
    choose_currency_callback = State()
    choose_currency_by_hand = State()


@router.callback_query(Text('converter', ignore_case=True))
async def converter_cmd(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(text="Выберите валюту, в которую будет переведена ваша валюта по умолчанию "
                                f"(<b><i>{await get_currency(callback.from_user.id)}</i></b>)",
                                chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                reply_markup=await make_keyboard(callback.from_user.id))
    await state.set_state(CurrencyChoice.choose_currency_callback)
    await callback.answer()


@router.callback_query(CurrencyChoice.choose_currency_callback, Text(startswith="curr_"))
async def convertation_to_currency(callback: CallbackQuery, bot: Bot, state: FSMContext):
    currency = callback.data.split("_")[1]
    if currency == 'byhand':
        await state.set_state(CurrencyChoice.choose_currency_by_hand)
        await bot.edit_message_text(text="Примеры формата ввода: <i>RUB</i>, <i>USD</i>, <i>EUR</i>\n\n"
                                    "Коды можно просмотреть "
                                    '<a href="https://www.geostat.ge/media/20898/9-Currency-Classification-ISO-4217-2015.pdf">здесь</a>',
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id)
    else:
        res = await convert(callback.from_user.id, currency)
        if res == "error":
            await bot.edit_message_text(text="На сервере произошла ошибка. Повторите операцию позднее.",
                                        chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=server_error_kb)
        else:
            await bot.edit_message_text(text=f"На данный момент 1 <b><i>{await get_currency(callback.from_user.id)}</i></b> = {res} <b><i>{currency}</i></b>",
                                        chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=convert_kb)
            await update_last_used_currency(callback.from_user.id, currency)
        await state.clear()
    await callback.answer()


@router.message(CurrencyChoice.choose_currency_by_hand, F.text, CurrencyInputCheck(), flags=flags)
async def currency_input_by_hand(message: Message, state: FSMContext):
    res = await convert(message.from_user.id, message.text)
    if res == 'error':
        await message.answer(text="На сервере произошла ошибка. Повторите операцию позднее.",
                             reply_markup=server_error_kb)
    else:
        await message.answer(
            text=f"На данный момент 1 <b><i>{await get_currency(message.from_user.id)}</i></b> = {res} <b><i>{message.text}</i></b>",
            reply_markup=convert_kb)
        await update_last_used_currency(message.from_user.id, message.text)
    await state.clear()


@router.message(CurrencyChoice.choose_currency_by_hand, flags=flags)
async def wrong_currency_input(message: Message):
    await message.answer("Ввод валюты некорректен! Попробуйте еще раз.")


@router.callback_query(Text('last_used', ignore_case=True))
async def last_used_curr(callback: CallbackQuery, bot: Bot):
    last_used_currency = await get_last_used_currency(callback.from_user.id)
    res = await convert(callback.from_user.id, last_used_currency)
    if res == "error":
        await bot.edit_message_text(text="На сервере произошла ошибка. Повторите операцию позднее.",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=server_error_kb)
    else:
        await bot.edit_message_text(text=f"На данный момент 1 <b><i>{await get_currency(callback.from_user.id)}</i></b> = {res} <b><i>{last_used_currency}</i></b>",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=convert_kb)
    await callback.answer()
