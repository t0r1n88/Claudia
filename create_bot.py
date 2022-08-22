from aiogram import Bot
# импортируем диспетчер, класс который позволяет реагировать на собыьтия
from aiogram.dispatcher import Dispatcher
import os
import asyncio
import logging
from config import TOKEN



logging.basicConfig(level=logging.DEBUG)

# Текущий цикл событий. Для предотвращения флудинга
# https://aiogram-birdi7.readthedocs.io/en/latest/examples/throtling_example.html
loop = asyncio.get_event_loop()


# класс позволяет хранить данные в оперативной памяти
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# Инициализируем объект хранилища
storage = MemoryStorage()
# Инициализируем бота получаtv получем токен из файла конфигурации
# bot = Bot(token=os.getenv('TOKEN'),loop=loop)
bot = Bot(token=TOKEN,loop=loop)
# Инициализируем диспетчер
dp = Dispatcher(bot,storage=storage)
