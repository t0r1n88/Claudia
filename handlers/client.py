from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import keyboards.client_kb
from create_bot import bot, dp
from keyboards import kb_client
from data_base import sqlite_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import Throttled



"""*********************************КЛИЕНТСКАЯ ЧАСТЬ*************************************"""
"""************Машина состояний для регистрации на мероприятие"""
# Машина состояний для регистрации
class FSMReg_event(StatesGroup):
    """
    Класс для создания машины состояний регистрации на события
    """
    # Шаг с получением названия мероприятия
    name_event = State()
    # Шаг c получением контакта пользователя
    contact = State()

class FSMConfirm_presense(StatesGroup):
    """
    Класс для создания машины состояний для отправки геометки. ТАкое решение выбрано чтобы было проще воспользоваться кнопкой request_location

    """
    # Шаг с получение названия мероприятия для последующего запроса
    name_event = State()
    # Шаг с получением геолокации
    location = State()


# Обработчик команд
# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    # Хэндлер стартовых команд
    # Добавляем обработку ошибки в случае если пользователь не добавился к боту
    # Получаем айди пользователя и отправляем ему сообщение
    try:
        await bot.send_message(message.from_user.id,
                               'Добро пожаловать в Центр опережающей профессиональной подготовки Республики Бурятия!\n\n'
                               'Для работы используйте кнопки расположенные внизу экрана вашего телефона(компьютера).',
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
    # Вариант с контролем флуда. То есть на случай если пользователь будет много раз нажимать кнопку
    # Взято отсюда https://aiogram-birdi7.readthedocs.io/en/latest/examples/throtling_example.html
    try:
        # Execute throttling manager with rate-limit equal to 2 seconds for key "start"
        await dp.throttle('Режим_работы', rate=2)
    except Throttled:
        # If request is throttled, the `Throttled` exception will be raised
        await message.reply('Остановитесь! Подождите 2 секунды!')
    else:
        # если проверка на флуд пройдена то начинаем работу
        try:
            await bot.send_message(message.from_user.id, 'Пн-Пт с 9:00 до 18:00, Сб-Вс выходные')
            await message.delete()
        except:
            await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')





    #Старый вариант
    # try:
    #     await bot.send_message(message.from_user.id, 'Пн-Пт с 9:00 до 18:00, Сб-Вс выходные')
    #     await message.delete()
    # except:
    #     await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


# @dp.message_handler(commands=['Контакты'])
async def adress_copp(message: types.Message):
    """
    Обработка команды контакты
    """
    # Вариант с контролем флуда. То есть на случай если пользователь будет много раз нажимать кнопку
    # Взято отсюда https://aiogram-birdi7.readthedocs.io/en/latest/examples/throtling_example.html
    try:
        # Execute throttling manager with rate-limit equal to 2 seconds for key "start"
        await dp.throttle('Контакты', rate=2)
    except Throttled:
        # If request is throttled, the `Throttled` exception will be raised
        await message.reply('Остановитесь! Подождите 2 секунды!')
    else:
        # если проверка на флуд пройдена то начинаем работу
        try:
            await bot.send_message(message.from_user.id,
                                   'Адрес: г. Улан-Удэ, Гагарина 28а,Рабочий телефон: +7(3012)56-10-88')
            await message.delete()
        except:
            await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


    #Старый вариант
    # try:
    #     await bot.send_message(message.from_user.id,
    #                            'Адрес: г. Улан-Удэ, Гагарина 28а,Рабочий телефон: +7(3012)56-10-88')
    #     await message.delete()
    # except:
    #     await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/Application_to_COPP_BOT')


#
async def course_menu(message: types.Message):
    try:
        # Execute throttling manager with rate-limit equal to 2 seconds for key "start"
        await dp.throttle('На_что_можно_записаться', rate=2)
    except Throttled:
        # If request is throttled, the `Throttled` exception will be raised
        await message.reply('Остановитесь! Подождите 2 секунды!')
    else:
        # если проверка на флуд пройдена то начинаем работу
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

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('rem '))
async def cancel_registered_callback_run(callback_query:types.CallbackQuery):

    # Получаем айди нужного мероприятия
    id_event = callback_query.data.replace('rem ', '')
    # Получаем название нужного курса
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]
    id_participant = callback_query.from_user.id
    # Делаем запрос
    await sqlite_db.sql_cancel_reg_event(name_event,id_participant)
    await bot.send_message(callback_query.from_user.id,f'Регистрация на {name_event} отменена')
    # Подтверждаем завершение операции. Чтобы не крутились часы возле кнопки
    await callback_query.answer()




@dp.callback_query_handler(lambda x: x.data and x.data.startswith('conf '))
async def confirm_presence_callback_run(callback_query:types.CallbackQuery,state:FSMContext):
    """
    Функция для отправки геометки для подтверждения посещения мероприятия
    """
    # Получаем айди мероприятия на которое происходит записи
    id_event = callback_query.data.split()[1]
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]
    await FSMConfirm_presense.name_event.set()
    async with state.proxy() as data:
        data['name_event'] = name_event

    await FSMConfirm_presense.next()
    await callback_query.message.reply(
        'Нажмите кнопку Отправить где я,чтобы подтвердить свое присутствие на мероприятии \nЧтобы отказать от подтверждения напишите в чат слово отмена',
        reply_markup=keyboards.client_kb.kb_client_confirm_presense)
    await callback_query.answer()

async def confirm_presense(message:types.Message,state:FSMContext):
    """
    Функция для получения данных геолокации
    """
    async with state.proxy() as data:
        data['id_participant'] = message.from_user.id
        data['latitude'] = message.location.latitude
        data['longitude'] = message.location.longitude
        data['event_mark'] = message.date
    # Обновляем данные в таблице, если айди пользователя и имя мероприятия есть в таблице
    # Временный костыль
    if not await sqlite_db.sql_check_exists_app(data['name_event'], data['id_participant']) == (0,):
        await sqlite_db.sql_confirm_presense_on_location(state)
        await state.finish()
        await message.answer(f'Подтверждение вашего присутствия на {data["name_event"]} принято', reply_markup=keyboards.client_kb.kb_client)
    else:
        await bot.send_message(message.from_user.id, f'Сначала зарегистрируйтесь на {data["name_event"]}',
                               reply_markup=keyboards.client_kb.kb_client)
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('reg '))
async def sign_event_callback_run(callback_query: types.CallbackQuery,state:FSMContext):
    # Получаем айди мероприятия на которое происходит записи
    id_event = callback_query.data.split()[1]
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]
    await FSMReg_event.name_event.set()
    async with state.proxy() as data:
        data['name_event'] = name_event
    await FSMReg_event.next()
    await callback_query.message.reply(
        'Нажмите кнопку Поделиться номером,чтобы зарегистрироваться \nЧтобы отказать от регистрации напишите в чат слово отмена',
        reply_markup=keyboards.client_kb.kb_client_reg)
    await callback_query.answer()

async def cancel_handler_reg_event(message: types.Message, state: FSMContext):
    # получаем текущее состояние машины состояний
    current_state = await state.get_state()
    # Если машина не находится в каком либо состоянии то ничего не делаем, в противном случае завершаем машину состояний
    if current_state is None:
        return
    await state.finish()
    await message.reply('Процесс отменен',reply_markup=keyboards.client_kb.kb_client)

async def sign_event_contact(message:types.Message,state:FSMContext):
    if message.from_user.id == message.contact.user_id:
        async with state.proxy() as data:
            data['id_participant'] = message.from_user.id
            data['phone'] = message.contact.phone_number
            data['first_name'] = message.contact.first_name
            data['last_name'] = message.contact.last_name
        # Временный костыль
        if await sqlite_db.sql_check_exists_app(data['name_event'],data['id_participant']) == (0,):
            await sqlite_db.sql_add_reg_on_event(state)
            await message.answer(f'Вы записаны на мероприятие {data["name_event"]}',reply_markup=keyboards.client_kb.kb_client)

            await state.finish()
        else:
            await bot.send_message(message.from_user.id,f'Вы УЖЕ записаны на {data["name_event"]}',reply_markup=keyboards.client_kb.kb_client)
            await state.finish()

    else:
        await bot.send_message(message.from_user.id, ' Отправьте СВОИ данные!')

def register_handlers_client(dp: Dispatcher):
    """
    Регистрируем хэндлеры клиента чтобы не писать над каждой функцией декоратор с командами
    """
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(cancel_handler_reg_event, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler_reg_event, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(sign_event_callback_run,state=FSMReg_event.name_event)
    # Машина состояний для регистрации на мероприятие
    dp.register_message_handler(confirm_presence_callback_run,state=FSMConfirm_presense.name_event)
    dp.register_message_handler(confirm_presense,content_types=['location'],state=FSMConfirm_presense.location)
    dp.register_message_handler(sign_event_contact,content_types=['contact'],state=FSMReg_event.contact)

    dp.register_message_handler(working_regime, commands=['Режим_работы'])
    dp.register_message_handler(adress_copp, commands=['Контакты'])
    dp.register_message_handler(course_menu, commands=['На_что_можно_записаться'])



