import pandas as pd
import numpy as np
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards.admin_kb
from create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
from geopy.distance import geodesic as GD


# Создаем константу для айди пользователя по которой будем определять является ли пользователь админом
ID = None


def calculate_distanse(row):
    """
    Функция для подсчета дистванции
    """
    if None not in row['location']:
        return GD(row['event_location'], row['location']).m
    else:
        return None

class FSMAdmin(StatesGroup):
    """
    Класс в котором мы создаем состояния для шагов машины состояний
    """
    # Состояния которые будут использоваться в процессе загрузки нового курса
    photo_course = State()
    name_course = State()
    description_course = State()
    how_sign_course = State()
    event_mark = State()

class FSMReportAdmin(StatesGroup):
    """
    Класс в котором хранятся шаги машины состояний посещаемости
    """
    # состояния которые будут использоваться при обработке посещаемости
    name_event = State()
    event_location = State()
    time_begin_event = State()
    time_end_event = State()
    distance_event = State()
    create_report = State()


# проверяем пользователя на права администратора в группе
# @dp.message_handler(commands=['admin'],is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    # Получаем айди пользователя
    ID = message.from_user.id
    # Отправляем сообщение через бота в личку пользователю
    await bot.send_message(message.from_user.id, 'Ожидаю ваших команд', reply_markup=admin_kb.kb_admin_course)
    await message.delete()


# Начало диалога загрузки нового курса
# Для начала работы требуем прописать команду Загрузить. состояние машины состояний(ха) инициаизируется None
# @dp.message_handler(commands='Загрузить',state=None)
async def load_course(message: types.Message):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        # Переводим машину состояний в первую стадию загрузка фото курса
        await FSMAdmin.photo_course.set()
        # Пишем сообщение пользователю, что ему нужно загрузить фото
        await message.reply('Загрузите фото курса\nЧтобы прекратить загрузку напишите в чат слово отмена')


# Добавляем обязательную кнопку для выхода из машины состояний
# "*" означает любое состояние машины состояний
# 2 декоратора нужны чтобы можно было отменить как прописав команду через \ так и просто написав слово отмена
# @dp.message_handler(state="*",commands='отмена')
# @dp.message_handler(Text(equals='отмена',ignore_case=True),state="*")
async def cancel_handler_load_course(message: types.Message, state: FSMContext):
    # получаем текущее состояние машины состояний
    current_state = await state.get_state()
    # Если машина не находится в каком либо состоянии то ничего не делаем, в противном случае завершаем машину состояний
    if current_state is None:
        return
    await state.finish()
    await message.reply('Загрузка курса(события) отменена')


# получаем ответ пользователя и записываем в словарь
# ограничиваем загрузку только фото и указываем что машина состояний должна находиться в стадии photo_course
# @dp.message_handler(content_types=['photo'],state=FSMAdmin.photo_course)
async def load_photo_course(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Через контекстный менеджер получаем записываем в словарь  айди загруженной картинки
            data['img_course'] = message.photo[0].file_id
            # Переводим машину состояний в следующую фазу
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести название курса
        await message.reply('Введите название курса\nЧтобы прекратить загрузку напишите в чат слово отмена')


# Получаем от пользователя название курса
# @dp.message_handler(state=FSMAdmin.name_course)
async def load_name_course(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        # К Через контекстный менеджер записываем с словарь название курса
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['name_course'] = message.text
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести описание курса
        await message.reply('Введите описание курса\nЧтобы прекратить загрузку напишите в чат слово отмена')


# Получаем от пользователя описание курса
# @dp.message_handler(state=FSMAdmin.description_course)
async def load_description_course(message: types.Message, state: FSMContext):
    # К Через контекстный менеджер записываем в словарь описание курса
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['description_course'] = message.text
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести сведения о том кто может записаться и как записаться
        await message.reply('Введите кто,как и на каких условиях может записаться на курс\nЧтобы прекратить загрузку напишите в чат слово отмена')


# Получаем от пользователя описание того как записаться на курс
# @dp.message_handler(state=FSMAdmin.how_sign_course)
async def load_how_sign_course(message: types.Message, state: FSMContext):
    # К Через контекстный менеджер записываем в словарь как записаться на курс
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['how_sign_course'] = message.text
        # Переводим машину в следующее состояние
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести сведения о типе мероприятия
        await message.reply('Введите да, если это событие\nВведите нет,если это обычный курс\nЧтобы прекратить загрузку напишите в чат слово отмена')


# Получаем от пользователя явлется ли курс мероприятием
async def load_event_mark_course(message:types.Message,state: FSMContext):
    # К Через контекстный менеджер записываем в словарь является ли курс мероприятием
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        check_message_text = message.text.lower()
        # проверка правильности ввода
        if check_message_text == 'да' or check_message_text == 'нет':
            async with state.proxy() as data:
                data['event_mark'] = check_message_text
            # Заканчиваем переходы по состояниям
            # После выполнения этой команды словарь data очищается.Поэтому нужно сохранить данные

            await sqlite_db.sql_add_course(state)
            await message.answer('Данные курса(мероприятия) добавлены')

            await state.finish()
        else:
            await message.reply('Введите да, если это событие\nВведите нет,если это обычный курс')


# Декоратор для ответа на  команду на удаление. Т.е если запрос будет не пустой и он будет начинаться с del то функция выполнится
# Более понятное объяснение https://youtu.be/gpCIfQUbYlY?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_course_callback_run(callback_query: types.CallbackQuery):
    deleted_course = callback_query.data.replace('del ', '')
    # Отправляем строку вида del название курса в функцию для удаления из базы данных.Передтэтим очищаем от del
    await sqlite_db.sql_delete_course(deleted_course)
    await callback_query.answer(f'Курс  удален', show_alert=True)
    await callback_query.answer()

async def delete_course(message: types.Message):
    """
    Функция для удаления курса из базы данных
    """
    if message.from_user.id == ID:
        # Получаем из таблицы данные всех курсов
        all_course_data = await sqlite_db.sql_read_all_courses()
        # Итерируемся по полученному списку кортежей
        for course in all_course_data:
            # Создаем инлайн кнопку
            # inline_del_course_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}'))
            # Отправляем данные курса из таблицы
            await bot.send_photo(message.from_user.id, course[1],
                                 f'{course[2]}\nОписание курса: {course[3]}\n Условия записи на курс: {course[4]}')
            # Отправляем инлайн кнопку вместе с сообщением
            # await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}')))
            await bot.send_message(message.from_user.id,text='Нажмите кнопку для удаления курса',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить курс {course[2]}', callback_data=f'del {course[0]}')))


async def report_event(message:types.Message):
    """
    Функция для получения списка зарегистристрировшихся и списка тех кто был на мероприятии
    """
    if message.from_user.id == ID:
        # Получаем из таблицы данные всех курсов
        all_course_data = await sqlite_db.sql_read_all_courses()

        # Итерируемся по полученному списку кортежей
        for course in all_course_data:
            # Проверяем признак является ли курс мероприятием
            if course[5] == 'да':
                btn_inline_list_registered = InlineKeyboardButton(f'Записавшиеся', callback_data=f'get reg {course[0]}')
                btn_inline_list_participants = InlineKeyboardButton(f'Присутствующие', callback_data=f'get par {course[0]}')
                x = [btn_inline_list_registered, btn_inline_list_participants]
                inline_stat_kb = InlineKeyboardMarkup().row(*x)
                # Если это мероприятие то отправляем администратору сообщение и клавиатуру для работы
                await bot.send_photo(message.from_user.id, course[1],
                                     f'{course[2]}\nОписание курса: {course[3]}\n Условия записи на курс: {course[4]}')
                # Отправляем инлайн кнопку вместе с сообщением
                await bot.send_message(message.from_user.id, text='Нажмите нужную кнопку', reply_markup=inline_stat_kb)

# Декоратор для ответа на  команду получения таблицы записавшихся на мероприятие
# Более понятное объяснение https://youtu.be/gpCIfQUbYlY?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('get reg'))
async def get_registered_callback_run(callback_query: types.CallbackQuery):
    # Получаем айди нужного мероприятия
    id_event = callback_query.data.replace('get reg ', '')
    # Получаем название нужного курса
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]
    await sqlite_db.sql_get_registered(name_event)
    with open(f'Список зарегистрировашихся на {name_event}.xlsx','rb') as file:
        await bot.send_document(callback_query.from_user.id,file)
    await callback_query.answer(f'Скачайте файл с данными зарегистрировавшихся', show_alert=True)
    await callback_query.answer()


# Запускаем машину состояний посещаемости
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('get par'))
async def get_confirmed_callback_run(callback_query: types.CallbackQuery,state:FSMContext):
    # Получаем айди нужного мероприятия
    id_event = callback_query.data.replace('get par ', '')
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # Получаем название мероприятия
    name_event = tuple_name_event[0]
    # Запускаем машину состояний
    await FSMReportAdmin.name_event.set()
    # записываем название мероприятия
    async with state.proxy() as data:
        data['name_event'] = name_event

    # Переходим на следующий шаг
    await FSMReportAdmin.next()
    # Отправляем запрос на локацию
    await callback_query.message.reply('Нажмите кнопку Отправить локацию мероприятия\n чтобы прекратить создание отчета напишите в чат слово отмена',
                                       reply_markup=keyboards.admin_kb.kb_admin_event_location)
    await callback_query.answer()
async def set_event_location(message:types.Message,state:FSMContext):
    """
    Функция для установки геолокации мероприятия
    """
    async with state.proxy() as data:
        data['event_location_latitude'] = message.location.latitude
        data['event_location_longitude'] = message.location.longitude
    await FSMReportAdmin.next()

    await message.reply('Введите дату и время НАЧАЛА мероприятия в формате день.месяц.год час.минута.секунда\n'
                        'Например 12.07.2022 14.35.00',reply_markup=types.ReplyKeyboardRemove())

async def set_time_begin_event(message:types.Message,state:FSMContext):
    """
    Функция для установки даты начала мероприятия
    """
    # Проверяем корректность введенного текста. Конечно можно было использовать регулярку, но проще будет try except
    try:
        time_begin_event = datetime.datetime.strptime(message.text,"%d.%m.%Y %H.%M.%S")
        async with state.proxy() as data:
            data['time_begin_event'] = time_begin_event
        await FSMReportAdmin.next()
        await message.reply('Введите дату и время ОКОНЧАНИЯ мероприятия в формате день.месяц.год час.минута.секунда\n'
                        'Например 12.07.2022 14.35.00')

    except ValueError:
        await message.reply('Проверьте корректность введенных данных!!!в формате день.месяц.год час.минута.секунда\n'
                        'Например 12.07.2022 14.35.00')

async def set_time_end_event(message:types.Message,state:FSMContext):
    """
    Функция для установки даты окончания мероприятия
    """
    # Проверяем корректность введенного текста. Конечно можно было использовать регулярку, но проще будет try except
    try:
        time_end_event = datetime.datetime.strptime(message.text,"%d.%m.%Y %H.%M.%S")
        async with state.proxy() as data:
            data['time_end_event'] = time_end_event
        await FSMReportAdmin.next()
        await message.reply('Введите расстояние в метрах, все участники расстояние между геометками которых и геометкой мероприятия будут меньше этого значения\n будут считаться посетившими мероприятие \n'
                        'Например 200. Не забывайте что погрешность геолокации в среднем 50 метров')

    except ValueError:
        await message.reply('Проверьте корректность введенных данных!!!в формате день.месяц.год час.минута.секунда\n'
                        'Например 12.07.2022 14.35.00')

async def set_distance_event(message:types.Message,state:FSMContext):
    """
    Функция для установки допустимой дистацнии присутствия
    """
    # Проверяем корректность ввода
    try:
        distance = int(message.text)
        async with state.proxy() as data:
            data['distance_event'] = distance
        await message.reply('Отправьте любой символ чтобы начать обработку данных')
        await FSMReportAdmin.next()

    except ValueError:
        await message.reply('Проверьте введенные данные!!! Введите только ЦИФРЫ!!!')

async def processing_report_participants(message:types.Message,state:FSMContext):
    """
    Функция для создания самого отчета
    """

    async with state.proxy() as data:
    # Получаем список кортежей с заявками на нужное мероприятие
        all_app = await sqlite_db.sql_get_confirmed(data['name_event'])
        # превращаем его в датафрейм
        df = pd.DataFrame(all_app,columns=['app_id','name_event','id_participant','phone','first_name','last_name'
            ,'latitude','longitude','time_mark'])

        # конвертируем колонку time_mark к формату времени
        df['time_mark'] = pd.to_datetime(df['time_mark'])
        # сохраняем в переменные даты начала и окончания мероприятия,чтобы было легче проверять
        begin_date = data['time_begin_event']
        end_date = data['time_end_event']
        # конвертируем строку в datetime
        # time_begin_event = datetime.datetime.strptime(begin_date, "%d.%m.%Y %H.%M.%S")
        # time_end_event = datetime.datetime.strptime(end_date, "%d.%m.%Y %H.%M.%S")
        time_begin_event = data['time_begin_event']
        time_end_event = data['time_end_event']



        # Добавляем колонки из data и создаем колонки в датафрейме
        df['event_location_latitude'] = data['event_location_latitude']
        df['event_location_longitude'] = data['event_location_longitude']
        df['event_location'] = list(zip(df['event_location_latitude'], df['event_location_longitude']))
        df['location'] = list(zip(df['latitude'], df['longitude']))
        df['time_begin_event'] = data['time_begin_event']
        df['time_end_event'] = data['time_end_event']
        df['threshold_distance'] = data['distance_event']
        df['distance'] = df.apply(calculate_distanse, axis=1)
        # Округляем значения
        df['distance'] = df['distance'].apply(np.floor)
        # Считаем входит ли время отправки подтверждения в нужный диапазон
        df['time_result'] = df['time_mark'].apply(lambda x: time_begin_event <= x <= time_end_event)
        # Сравниваем полученное расстояние геометки пользователя и геометки мероприятия с установленным пределом
        df['distance_result'] = df['distance'] <= df['threshold_distance']
        # Формируем итоговый результат
        df['confrim'] = (df['time_result'] == True) & (df['distance_result'] == True)
        # Меняем булевы значения в датафрейме
        df.replace({True: 'Подтверждено', False: 'Не подтверждено'}, inplace=True)
        # Меняем названия колонок
        df.rename(columns={'app_id': 'Номер_заявки', 'name_event': 'Название_мероприятия', 'id_participant': 'id_участника',
                           'phone': 'Телефон',
                           'first_name': 'Имя', 'last_name': 'Фамилия', 'latitude': 'Широта_геометки_участника',
                           'longitude': 'Долгота_геометки_участника',
                           'time_mark': 'Дата_время_подтверждения',
                           'event_location_latitude': 'Широта_геометки_мероприятия',
                           'event_location_longitude': 'Долгота_геометка_мероприятия',
                           'event_location': 'Геометка_мероприятия', 'location': 'Геометка_участника',
                           'threshold_distance': 'Допустимое_расстояние_участия', 'distance': 'Итоговое_расстояние_участия',
                           'time_result': 'Участие_по_времени', 'distance_result': 'Участие_по_геометке',
                           'confrim': 'Подтверждение_участия', 'time_begin_event': 'Дата_начала_мероприятия',
                           'time_end_event': 'Дата_окончания_мероприятия'},
                  inplace=True)
        # Создаем сокращенный вариант отчета
        short_df = df[['Номер_заявки','Название_мероприятия','id_участника','Телефон','Имя','Фамилия','Подтверждение_участия']]
        # Сохраняем результат

        df.to_excel(f'Полный отчет посещаемости {data["name_event"]}.xlsx',index=False)
        short_df.to_excel(f'Краткий отчет посещаемости {data["name_event"]}.xlsx',index=False)

        with open(f'Полный отчет посещаемости {data["name_event"]}.xlsx','rb') as file:
            await bot.send_document(message.from_user.id,file)

        with open(f'Краткий отчет посещаемости {data["name_event"]}.xlsx','rb') as file1:
            await bot.send_document(message.from_user.id,file1)

        # выходим из маишны состояния
        await state.finish()
        await bot.send_message(message.from_user.id,'Скачайте нужный файл',reply_markup=keyboards.admin_kb.kb_admin_course)





# регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(load_course, commands='Загрузить', state=None)
    dp.register_message_handler(cancel_handler_load_course, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler_load_course, Text(equals='отмена', ignore_case=True), state="*")
    # Хэндлеры машины состояний загрузки курсов
    dp.register_message_handler(load_photo_course, content_types=['photo'], state=FSMAdmin.photo_course)
    dp.register_message_handler(load_name_course, state=FSMAdmin.name_course)
    dp.register_message_handler(load_description_course, state=FSMAdmin.description_course)
    dp.register_message_handler(load_how_sign_course, state=FSMAdmin.how_sign_course)
    dp.register_message_handler(load_event_mark_course,state=FSMAdmin.event_mark)
    # Хэндлеры машины состояний посещаемости
    dp.register_message_handler(get_confirmed_callback_run,state=FSMReportAdmin.name_event)
    dp.register_message_handler(set_event_location,content_types=['location'],state=FSMReportAdmin.event_location)
    dp.register_message_handler(set_time_begin_event,state=FSMReportAdmin.time_begin_event)
    dp.register_message_handler(set_time_end_event,state=FSMReportAdmin.time_end_event)
    dp.register_message_handler(set_distance_event,state=FSMReportAdmin.distance_event)
    dp.register_message_handler(processing_report_participants,state=FSMReportAdmin.create_report)

    dp.register_message_handler(delete_course, commands=['Удалить'])
    dp.register_message_handler(report_event,commands=['Отчетность'])
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
