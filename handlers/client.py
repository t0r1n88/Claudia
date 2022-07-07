from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from data_base import sqlite_db
from aiogram.dispatcher.filters.state import State, StatesGroup

"""*********************************КЛИЕНТСКАЯ ЧАСТЬ*************************************"""
"""************Машина состояний для регистрации на мероприятие"""
# Машина состояний для регистрации
class FSMReg_event(StatesGroup):
    """
    Класс для создания машины состояний регистрации на события
    """
    # Шаг с получением инфомрации о событии на которое происходит запись и айди пользователя
    id_user = State()
    # Шаг c получением контакта пользователя
    contact = State()





# Обработчик команд
# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    # Хэндлер стартовых команд
    # Добавляем обработку ошибки в случае если пользователь не добавился к боту
    # Получаем айди пользователя и отправляем ему сообщение
    try:
        await bot.send_message(message.from_user.id,
                               'Добро пожаловать в Центр опережающей профессиональной подготовки Республики Бурятия',
                               reply_markup=kb_client)
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


#
async def course_menu(message: types.Message):
    await sqlite_db.sql_read_course(message)


async def get_location(message: types.Message):
    """
    Функция для получения данных геолокации
    """
    if message.location is not None:
        await bot.send_message(message.from_user.id, message.location)
        await bot.send_message(message.from_user.id,
                               f'Широта {message.location.latitude}\n Долгота {message.location.longitude}')
    else:
        await bot.send_message(message.from_user.id, 'Возникла проблема с обработкой геолокации. Попробуйте позже')


async def get_contact(message: types.Message):
    if message.from_user.id == message.contact.user_id:
        await bot.send_message(message.from_user.id, message.contact.phone_number)
        await bot.send_message(message.from_user.id, message.contact.first_name)
    else:
        await bot.send_message(message.from_user.id, ' Отправьте СВОИ данные!')


# query_handlers для записи на мероприятие и подтверждения участия
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('reg '))
async def sign_event_callback_run(callback_query: types.CallbackQuery):
    # Получаем айди мероприятия на которое происходит записи
    id_event = callback_query.data.split()[1]
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]


    await callback_query.answer(f'Вы записались на  {name_event}', show_alert=True)



def register_handlers_client(dp: Dispatcher):
    """
    Регистрируем хэндлеры клиента чтобы не писать над каждой функцией декоратор с командами
    """
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(working_regime, commands=['Режим_работы'])
    dp.register_message_handler(adress_copp, commands=['Контакты'])
    dp.register_message_handler(course_menu, commands=['Текущие_курсы'])
    dp.register_message_handler(get_location, content_types=['location'])
    dp.register_message_handler(get_contact, content_types=['contact'])
