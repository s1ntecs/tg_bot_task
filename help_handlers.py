from aiogram import types, Dispatcher


# Функция-обработчик команды /start
async def send_welcome(message: types.Message):
    # Создаем клавиатуру с функциями бота
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = types.KeyboardButton("Погода")
    currency_button = types.KeyboardButton("Конвертер валют")
    poll_button = types.KeyboardButton("Опрос")
    cute_animals_button = types.KeyboardButton("Милые животные")
    keyboard.add(
        weather_button,
        currency_button,
        poll_button,
        cute_animals_button
        )

    # Отправляем сообщение с приветствием и клавиатурой
    await message.answer(
        "Привет! Я бот, который может сделать следующие вещи:",
        reply_markup=keyboard,
    )


async def handle_messages(message: types.Message):
    match message.text:
        case 'Погода':
            await message.answer("Чтобы узнать погоду, отправьте команду /weather")
        case 'Конвертер валют':
            await message.answer("Чтобы конвертировать валюту, отправьте команду /currency")
        case 'Опрос':
            await message.answer("Чтобы создать опрос, отправьте команду /poll")
        case 'Милые животные':
            await message.answer(
            "Чтобы получить смешную картинку с животными,"
            " отправьте команду /cute_animals"
            )

# Функция-обработчик команды /help
async def send_help(message: types.Message):
    # Отправляем сообщение с инструкцией по использованию бота
    await message.answer(
        "Я могу выполнять следующие команды:\n"
        "/start - начать работу с ботом\n"
        "/help - получить помощь\n"
        "/weather - узнать погоду в определенном городе\n"
        "/currency - конвертировать валюты\n"
        "/poll - создать опрос\n"
        "/cute_animals - получить случайную картинку с милыми животными"
    )


def register_main_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(send_help, commands=["help"])
