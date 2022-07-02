from aiogram import Bot
# импортируем диспетчер, класс который позволяет реагировать на собыьтия
from aiogram.dispatcher import Dispatcher
import os
# класс позволяет хранить данные в оперативной памяти
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# Инициализируем объект хранилища
storage = MemoryStorage()
# Инициализируем бота получая токен из переменной окружения
bot = Bot(token=os.getenv('TOKEN'))
# Инициализируем диспетчер
dp = Dispatcher(bot,storage=storage)
