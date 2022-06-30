# импортируем класс бота, класс для аннтоации типов
import json

from aiogram import Bot,types
# импортируем диспетчер, класс который позволяет реагировать на собыьтия
from aiogram.dispatcher import Dispatcher
# импортируем excecutor для запуска бота в онлайн
from aiogram.utils import executor
#Чтобы прочитать токен из созданной в батнике переменной среды окружения
import os,string

async def on_startup(_):
    """
    Функция выполняющая при старте бота, для подключения к базе данных

    """
    print('Бот вышел в онлайн')






# Инициализируем бота получая токен из переменной окружения
bot = Bot(token=os.getenv('TOKEN'))
# Инициализируем диспетчер
dp = Dispatcher(bot)







"""*********************************КЛИЕНТСКАЯ ЧАСТЬ*************************************"""
# Обработчик команд
@dp.message_handler(commands=['start','help'])
async def command_start(message :types.Message):
    # Хэндлер стартовых команд
    # Добавляем обработку ошибки в случае если пользователь не добавился к боту
    # Получаем айди пользователя и отправляем ему сообщение
    try:
        await bot.send_message(message.from_user.id,'Добро пожаловать в Центр опережающей профессиональной подготовки Республики Бурятия')
        # Удаляем сообщение чтобы не спамить в группе
        await message.delete()

    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')
@dp.message_handler(commands=['Режим_работы'])
async def working_regime(message : types.Message):
    """
    Обработка команды режим работы
    """
    try:
        await bot.send_message(message.from_user.id,'Пн-Пт с 9:00 до 18:00, Сб-Вс выходные')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


@dp.message_handler(commands=['Контакты'])
async def adress_copp(message:types.Message):
    """
    Обработка команды контакты
    """
    try:
        await bot.send_message(message.from_user.id,'Адрес: г. Улан-Удэ, Гагарина 28а,Рабочий телефон: +7(3012)56-10-88')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


@dp.message_handler()
async def echo_send(message : types.Message):
    # проверяем сообщение на мат. С помощью пересечения с множеством матов
    # ссылка на объяснение конструкции https://youtu.be/Lgm7pxlr7F0?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ
    if {word.lower().translate(str.maketrans('','',string.punctuation)) for word in message.text.split()}.intersection(set(json.load(open('cenz.json')))):
        await message.reply('Маты запрещены! Просим проявить уважение!!!')
        await message.delete()








# Запускаем бота
# skip_updates=True - для того чтобы бот не отвечал на сообщение пришедшие когда он бы не в онлайн
executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
