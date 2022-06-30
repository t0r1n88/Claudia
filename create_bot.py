from aiogram import Bot
# импортируем диспетчер, класс который позволяет реагировать на собыьтия
from aiogram.dispatcher import Dispatcher
import os

# Инициализируем бота получая токен из переменной окружения
bot = Bot(token=os.getenv('TOKEN'))
# Инициализируем диспетчер
dp = Dispatcher(bot)
