from aiogram import types,Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove



"""*********************************КЛИЕНТСКАЯ ЧАСТЬ*************************************"""


# Обработчик команд
# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    # Хэндлер стартовых команд
    # Добавляем обработку ошибки в случае если пользователь не добавился к боту
    # Получаем айди пользователя и отправляем ему сообщение
    try:
        await bot.send_message(message.from_user.id,
                               'Добро пожаловать в Центр опережающей профессиональной подготовки Республики Бурятия',reply_markup=kb_client)
        # Удаляем сообщение чтобы не спамить в группе
        await message.delete()

    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


# @dp.message_handler(commands=['Режим_работы'])
async def working_regime(message: types.Message):
    """
    Обработка команды режим работы
    """
    try:
        await bot.send_message(message.from_user.id, 'Пн-Пт с 9:00 до 18:00, Сб-Вс выходные')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


# @dp.message_handler(commands=['Контакты'])
async def adress_copp(message: types.Message):
    """
    Обработка команды контакты
    """
    try:
        await bot.send_message(message.from_user.id,
                               'Адрес: г. Улан-Удэ, Гагарина 28а,Рабочий телефон: +7(3012)56-10-88')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')

def register_handlers_client(dp :Dispatcher):
    """
    Регистрируем хэндлеры клиента чтобы не писать над каждой функцией декоратор с командами
    """
    dp.register_message_handler(command_start,commands=['start','help'])
    dp.register_message_handler(working_regime,commands=['Режим_работы'])
    dp.register_message_handler(adress_copp,commands=['Контакты'])