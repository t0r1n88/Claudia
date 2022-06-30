# импортируем класс бота, класс для аннтоации типов
from aiogram import Bot,types
# импортируем диспетчер, класс который позволяет реагировать на собыьтия
from aiogram.dispatcher import Dispatcher
# импортируем excecutor для запуска бота в онлайн
from aiogram.utils import executor
#Чтобы прочитать токен из созданной в батнике переменной среды окружения
import os
# token ='5549256746:AAHQ8_nqbihLpEkVN20zNro4I92c_JUr_9k'

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
        await message.reply('Общение с ботом через ЛС бота, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')
@dp.message_handler(commands=['Режим_работы'])
async def working_regime(message : types.Message):
    """
    Обработка команды режим работы
    """
    await bot.send_message(message.from_user.id,'Пн-Пт с 9:00 до 18:00, Сб-Вс выходные')
    await message.delete()

@dp.message_handler(commands=['Контакты'])
async def adress_copp(message:types.Message):
    """
    Обработка команды контакты
    """
    await bot.send_message(message.from_user.id,'Адрес: г. Улан-Удэ, Гагарина 28а,Рабочий телефон: +7(3012)56-10-88')
    await message.delete()




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
executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
