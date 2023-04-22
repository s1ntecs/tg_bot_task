from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import WEATHER_TOKEN
import aiohttp


class WeatherState(StatesGroup):
    waiting_for_city = State()


async def get_weather(message: types.Message):
    # Отправляем сообщение с просьбой ввести город
    await message.answer("Введите название города:")

    # Устанавливаем состояние ожидания ввода города
    await WeatherState.waiting_for_city.set()


async def process_weather_city(message: types.Message, state: FSMContext):
    # Получаем город из сообщения
    try:
        city = message.text

        # Формируем URL запроса для получения погоды
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}"
            f"&units=metric&appid={WEATHER_TOKEN}"
        )

        # Отправляем запрос и сохраняем ответ в JSON формате
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                weather_data = await response.json()

        # Если ответ содержит ошибку, отправляем сообщение об ошибке
        if weather_data["cod"] != 200:
            await message.answer(f"Ошибка: {weather_data['message']}")
        else:
            # Извлекаем информацию о погоде из ответа
            temperature = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]

            # Форматируем и отправляем сообщение с информацией о погоде
            weather_message = (
                f"Погода в городе {city}:\n\n"
                f"Температура: {temperature} градусов \n"
                f"Ощущается как: {feels_like} градусов\n"
                f"Влажность: {humidity}%"
            )
            await message.answer(weather_message)

        # Сбрасываем состояние FSM
        await state.finish()
    except aiohttp.ClientError as e:
        await message.answer(
            f"Произошла ошибка при запросе погоды: {str(e)}")
    except KeyError as e:
        await message.answer(
            f"Произошла ошибка при обработке ответа от API: {str(e)}")
    except Exception as e:
        await message.answer(f"Произошла неизвестная ошибка: {str(e)}")

def register_handlers_weather(dp: Dispatcher):
    """ Регистрируем обработчики команд. """
    dp.register_message_handler(get_weather, commands=["weather"])
    dp.register_message_handler(process_weather_city,
                                state=WeatherState.waiting_for_city)
