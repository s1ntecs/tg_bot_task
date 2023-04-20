import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

# Получаем токен нашего бота из переменной окружения
WEATHER_TOKEN = os.getenv('OPENWEATHERMAP_API_KEY')
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
