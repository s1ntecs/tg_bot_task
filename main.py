from aiogram.utils import executor
from aiogram import types
from create_bot import dp
from new_poll import register_handlers_poll
from currency import register_handlers_currency
from weather import register_handlers_weather
from random_animal import register_handlers_animal_img
from help_handlers import register_main_handlers, handle_messages

if __name__ == "__main__":
    register_handlers_poll(dp=dp)
    register_handlers_currency(dp=dp)
    register_handlers_weather(dp=dp)
    register_handlers_animal_img(dp=dp)
    register_main_handlers(dp=dp)
    dp.register_message_handler(handle_messages)
    executor.start_polling(dp, skip_updates=True)
