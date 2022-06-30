# импортируем класс бота, класс для аннтоации типов
from aiogram import Bot,types
# импортируем диспетчер, класс который позволяет реагировать на собыьтия
from aiogram.dispatcher import Dispatcher
# импортируем excecutor для запуска бота в онлайн
from aiogram.utils import executor
#Чтобы прочитать токен из созданной в батнике переменной среды окружения
import os
# token ='5549256746:AAHQ8_nqbihLpEkVN20zNro4I92c_JUr_9k'

# Инициализируем бота получая токен из переменной окружения
bot = Bot(token=os.getenv('TOKEN'))
# Инициализируем диспетчер
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_send(message : types.Message):
    #асинхронная штука подождать пока не появится свобоное место в потоке
    if 'Привет' in message.text:
        # await message.answer('Привет тебе от нас')
        # Способ по умолчанию. Отправляем эхо текст обратно пользователю
        # await message.answer(message.text)
        # Бот отвечает с упоминаем автора сообшения(как бы в ответ)

        await message.reply('Привет тебе от нас')
        # Бот отвечает сообщением в личку. Но нужно помнить что такое возможно только если пользователь уже писал боту.Бот не может первым писать пользователю
        # await bot.send_message(message.from_user.id,message.text)



# Запускаем бота
# skip_updates=True - для того чтобы бот не отвечал на сообщение пришедшие когда он бы не в онлайн
executor.start_polling(dp,skip_updates=True)
