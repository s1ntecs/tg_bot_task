from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiohttp


class Currency(StatesGroup):
    waiting_for_original_currency = State()
    waiting_for_target_currency = State()
    waiting_for_amount = State()


async def get_currency(message: types.Message):
    # Отправляем сообщение с просьбой ввести город
    await message.answer("Введите исходную валюту (например, USD):")

    # Устанавливаем состояние ожидания ввода валюту
    await Currency.waiting_for_original_currency.set()


async def convert_currency(message: types.Message, state: FSMContext):
    base_currency = message.text.upper()
    await state.update_data(base_currency=base_currency)
    await message.answer("Введите целевую валюту (например, EUR):")
    await Currency.waiting_for_target_currency.set()


async def process_target_currency(message: types.Message, state: FSMContext):
    target_currency = message.text.upper()
    await state.update_data(target_currency=target_currency)
    data = await state.get_data()
    base_currency = data.get("base_currency")
    target_currency = data.get("target_currency")

    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

    # Отправляем запрос и сохраняем ответ в JSON формате
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            currency_data = await response.json()

    # Если ответ содержит ошибку, отправляем сообщение об ошибке
    if response.status != 200:
        await message.answer("Ошибка: Не удалось получить курс валют.")
    else:
        # Извлекаем курс и конвертируем валюту
        exchange_rate = currency_data["rates"][target_currency]
        # Форматируем и отправляем сообщение с результатом конвертации
        currency_message = (
            f"1 {base_currency} ="
            f" {exchange_rate} {target_currency}"
            "\n\nВведите сумму для конвертации:"
        )
        await message.answer(currency_message)
        await state.update_data(exchange_rate=exchange_rate)
        # Ожидаем ответ пользователя и сохраняем его
        await Currency.waiting_for_amount.set()


async def process_amount(message: types.Message, state: FSMContext):
    amount = message.text
    data = await state.get_data()
    base_currency = data.get("base_currency")
    target_currency = data.get("target_currency")
    exchange_rate = data.get("exchange_rate")
    converted_amount = float(amount) * exchange_rate
    result_message = (f"{amount} {base_currency}"
                      f"{converted_amount:.2f}"
                      f"{target_currency}")
    await message.answer(result_message)

    await state.finish()


def register_handlers_currency(dp: Dispatcher):
    dp.register_message_handler(get_currency, commands=["currency"])
    dp.register_message_handler(convert_currency,
                                state=Currency.waiting_for_original_currency)
    dp.register_message_handler(process_target_currency,
                                state=Currency.waiting_for_target_currency)
    dp.register_message_handler(process_amount,
                                state=Currency.waiting_for_amount)
