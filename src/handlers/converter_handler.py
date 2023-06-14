from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.database.db import (get_currency, update_last_used_currency, get_last_used_currency,
                             update_number_of_requests, get_number_of_requests, ban_user, get_user_state,
                             set_banned_time, get_banned_time)
from src.keyboards.converter_keyboard import make_keyboard, convert_kb, server_error_kb
from src.functions.converter_func import convert
from src.filters.registration_filters import CurrencyInputCheck
from src.middlewares.ban_middleware import CheckIfBanned


router = Router()
flags = {"long_operation": "typing"}
router.callback_query.middleware(CheckIfBanned())


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
    if await get_number_of_requests(callback.from_user.id) >= 5:
        await ban_user(callback.from_user.id)
        await set_banned_time(callback.from_user.id, datetime.now().strftime("%H:%M"))
        await bot.edit_message_text(text="Вы привысили лимит запросов. Вы заблокированы на 10 минут.",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=server_error_kb)
    else:
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
                await bot.edit_message_text(text=f"На данный момент 1 <b><i>{currency}</i></b> = {res} <b><i>{await get_currency(callback.from_user.id)}</i></b>",
                                            chat_id=callback.from_user.id,
                                            message_id=callback.message.message_id,
                                            reply_markup=convert_kb)
                await update_last_used_currency(callback.from_user.id, currency)
            await state.clear()
        await callback.answer()
        await update_number_of_requests(callback.from_user.id)


@router.message(CurrencyChoice.choose_currency_by_hand, F.text, CurrencyInputCheck(), flags=flags)
async def currency_input_by_hand(message: Message, state: FSMContext):
    if await get_number_of_requests(message.from_user.id) >= 5:
        await message.answer(text="Вы привысили лимит запросов. Вы заблокированы на 10 минут.",
                             reply_markup=server_error_kb)
        await ban_user(message.from_user.id)
        await set_banned_time(message.from_user.id, datetime.now().strftime("%H:%M"))
    else:
        res = await convert(message.from_user.id, message.text)
        if res == 'error':
            await message.answer(text="На сервере произошла ошибка. Повторите операцию позднее.",
                                reply_markup=server_error_kb)
        else:
            await message.answer(
                text=f"На данный момент 1 <b><i>{message.text}</i></b> = {res} <b><i>{await get_currency(message.from_user.id)}</i></b>",
                reply_markup=convert_kb)
            await update_last_used_currency(message.from_user.id, message.text)
        await state.clear()
        await update_number_of_requests(message.from_user.id)
    

@router.message(CurrencyChoice.choose_currency_by_hand, flags=flags)
async def wrong_currency_input(message: Message):
    await message.answer("Ввод валюты некорректен! Попробуйте еще раз.")


@router.callback_query(Text('last_used', ignore_case=True))
async def last_used_curr(callback: CallbackQuery, bot: Bot):
    if await get_number_of_requests(callback.from_user.id) >= 5:
        await bot.edit_message_text(text="Вы привысили лимит запросов. Вы заблокированы на 10 минут.",
                                    chat_id=callback.from_user.id,
                                    message_id=callback.message.message_id,
                                    reply_markup=server_error_kb)
        await ban_user(callback.from_user.id)
        await set_banned_time(callback.from_user.id, datetime.now().strftime("%H:%M"))
    else:
        last_used_currency = await get_last_used_currency(callback.from_user.id)
        res = await convert(callback.from_user.id, last_used_currency)
        if res == "error":
            await bot.edit_message_text(text="На сервере произошла ошибка. Повторите операцию позднее.",
                                        chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=server_error_kb)
        else:
            await bot.edit_message_text(text=f"На данный момент 1 <b><i>{last_used_currency}</i></b> = {res} <b><i>{await get_currency(callback.from_user.id)}</i></b>",
                                        chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=convert_kb)
        await callback.answer()
        await update_number_of_requests(callback.from_user.id)
