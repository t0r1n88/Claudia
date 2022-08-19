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
import time
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
    visible = State()

class FSMEditCourseAdmin(StatesGroup):
    """
    Класс для машины состояний редактирования курсов.
    """
    id_course = State()
    photo_course = State()
    name_course = State()
    description_course = State()
    how_sign_course = State()
    event_mark = State()
    visible = State()

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

class FSMLoadNews(StatesGroup):
    """
    Класс в котором хранятся шаги машины состояний создания новости
        """
    img_news = State()
    description_news = State()

class FSMEditNews(StatesGroup):
    """
    Класс в котором хранятся шаги машины состояний для редактирования новости
    Пришлось его сделать поскольку для редактирования мне нужно где то хранить айди новости а в классе загрузки новости такое делать смысла нет
    """
    id_news = State()
    img_news = State()
    description_news = State()


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
        await message.reply('Загрузите фото курса\nЧтобы прекратить загрузку напишите в чат слово стоп')


# Добавляем обязательную кнопку для выхода из машины состояний
# "*" означает любое состояние машины состояний
# 2 декоратора нужны чтобы можно было отменить как прописав команду через \ так и просто написав слово отмена
# @dp.message_handler(state="*",commands='отмена')
# @dp.message_handler(Text(equals='отмена',ignore_case=True),state="*")
async def admin_cancel_handler_load_course(message: types.Message, state: FSMContext):
    # получаем текущее состояние машины состояний
    current_state = await state.get_state()
    # Если машина не находится в каком либо состоянии то ничего не делаем, в противном случае завершаем машину состояний
    if current_state is None:
        return
    await state.finish()
    await message.reply('Процесс прерван',reply_markup=admin_kb.kb_admin_course)

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
        await message.reply('Введите название курса\nЧтобы прекратить загрузку напишите в чат слово стоп')


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
        await message.reply('Введите описание курса\nЧтобы прекратить загрузку напишите в чат слово стоп')


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
        await message.reply('Введите кто,как и на каких условиях может записаться на курс\nЧтобы прекратить загрузку напишите в чат слово стоп')


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
        await message.reply('Введите да, если это событие\nВведите нет,если это обычный курс\nЧтобы прекратить загрузку напишите в чат слово стоп')


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
            # Переводим машину в следующее состояние
            await FSMAdmin.next()
            await message.reply('Введите да, чтобы сделать курс видимым\nВведите нет,если чтобы скрыть курс\nЧтобы прекратить загрузку напишите в чат слово стоп')

        else:
            await message.reply('Введите да, если это событие\nВведите нет,если это обычный курс')
# Получаем от пользователя нужно ли показывать курс
async def load_event_visible_course(message:types.Message,state: FSMContext):
    # К Через контекстный менеджер записываем в словарь является ли курс мероприятием
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        check_message_text = message.text.lower()
        # проверка правильности ввода
        if check_message_text == 'да' or check_message_text == 'нет':
            async with state.proxy() as data:
                data['visible'] = check_message_text
            await sqlite_db.sql_add_course(state)
            await message.answer('Данные курса(мероприятия) добавлены')
            await state.finish()
        else:
            await message.reply('Введите да, чтобы сделать курс видимым\nВведите нет,если чтобы скрыть курс\nЧтобы прекратить загрузку напишите в чат слово стоп')


# Декоратор для ответа на  команду на удаление. Т.е если запрос будет не пустой и он будет начинаться с hide то функция выполнится
# Более понятное объяснение https://youtu.be/gpCIfQUbYlY?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('hide '))
async def hide_course_callback_run(callback_query: types.CallbackQuery):
    id_course = callback_query.data.replace('hide ', '')
    # Отправляем строку вида del название курса в функцию для удаления из базы данных.Передтэтим очищаем от del
    await sqlite_db.sql_hide_course(id_course)
    await callback_query.answer(f'Курс скрыт', show_alert=True)
    await callback_query.answer()

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('show '))
async def show_course_callback_run(callback_query: types.CallbackQuery):
    id_course = callback_query.data.replace('show ', '')

    await sqlite_db.sql_show_course(id_course)
    await callback_query.answer(f'Курс отображается', show_alert=True)
    await callback_query.answer()


async def dysplay_course(message: types.Message):
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
            await bot.send_message(message.from_user.id,f'{course[2]}')
            # Отправляем инлайн кнопку вместе с сообщением
            # await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}')))
            await bot.send_message(message.from_user.id,text='Нажмите кнопку чтобы отобразить,скрыть,изменить курс',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Отображать курс {course[2]}', callback_data=f'show {course[0]}')).add(InlineKeyboardButton(f'Скрыть курс {course[2]}', callback_data=f'hide {course[0]}')).add(
                                       InlineKeyboardButton(f'Изменить курс {course[2]}',
                                                            callback_data=f'edit {course[0]}'))
                                   )


            # await bot.send_photo(message.from_user.id, course[1],
            #                      f'{course[2]}\nОписание курса: {course[3]}\n Условия записи на курс: {course[4]}')
            # # Отправляем инлайн кнопку вместе с сообщением
            # # await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}')))
            # await bot.send_message(message.from_user.id,text='Нажмите кнопку для удаления курса',
            #                        reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить курс {course[2]}', callback_data=f'del {course[0]}')))




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
    id_course = callback_query.data.replace('get reg ', '')
    # Получаем название нужного курса
    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sqlite_db.sql_read_name_course(id_course))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]
    await sqlite_db.sql_get_registered(id_course)
    with open(f'Список зарегистрировашихся на {name_event}.xlsx','rb') as file:
        await bot.send_document(callback_query.from_user.id,file)
    await callback_query.answer(f'Скачайте файл с данными зарегистрировавшихся', show_alert=True)
    await callback_query.answer()


# Запускаем машину состояний посещаемости
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('get par'))
async def get_confirmed_callback_run(callback_query: types.CallbackQuery,state:FSMContext):
    # Получаем айди нужного мероприятия
    id_course = callback_query.data.replace('get par ', '')
    # # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    # tuple_name_event = await (sqlite_db.sql_read_name_course(id_event))
    # # Получаем название мероприятия
    # name_event = tuple_name_event[0]
    # # Запускаем машину состояний
    await FSMReportAdmin.name_event.set()
    # записываем название мероприятия
    async with state.proxy() as data:
        data['id_course'] = id_course

    # Переходим на следующий шаг
    await FSMReportAdmin.next()
    # Отправляем запрос на локацию
    await callback_query.message.reply('Нажмите кнопку Отправить локацию мероприятия\n чтобы прекратить создание отчета напишите в чат слово стоп',
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
                        'Например 200. Не забывайте что погрешность геолокации в среднем 150 метров')

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
        all_app = await sqlite_db.sql_get_confirmed(data['id_course'])
        # превращаем его в датафрейм
        df = pd.DataFrame(all_app,columns=['app_id','id_course','id_participant','phone','first_name','last_name','reg_time_mark'
            ,'latitude','longitude','time_mark'])

        # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
        tuple_name_event = await (sqlite_db.sql_read_name_course(data['id_course']))
        # Распаковываем кортеж
        name_event = tuple_name_event[0]
        # Присваиваем колонке с айди курса -его название
        df['id_course'] = name_event

        # конвертируем колонку reg_time_event,time_mark к формату времени
        df['time_mark'] = pd.to_datetime(df['time_mark'])
        df['reg_time_mark'] = pd.to_datetime(df['reg_time_mark'])


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
        # Округляем значения. Также проверяем пустые значения для тех пользователей кто не заполнил геометки
        df['distance'] = df['distance'].apply(lambda x:np.floor(x) if type(x) == 'float' else x)
        # Считаем входит ли время отправки подтверждения в нужный диапазон
        df['time_result'] = df['time_mark'].apply(lambda x: time_begin_event <= x <= time_end_event)
        # Сравниваем полученное расстояние геометки пользователя и геометки мероприятия с установленным пределом
        df['distance_result'] = df['distance'] <= df['threshold_distance']
        # Формируем итоговый результат
        df['confrim'] = (df['time_result'] == True) & (df['distance_result'] == True)
        # Меняем булевы значения в датафрейме
        df.replace({True: 'Подтверждено', False: 'Не подтверждено'}, inplace=True)
        # Меняем названия колонок
        df.rename(columns={'app_id': 'Номер_заявки', 'id_course': 'Название_мероприятия', 'id_participant': 'id_участника',
                           'phone': 'Телефон',
                           'first_name': 'Имя', 'last_name': 'Фамилия','reg_time_mark':'Дата_регистрации', 'latitude': 'Широта_геометки_участника',
                           'longitude': 'Долгота_геометки_участника',
                           'time_mark': 'Дата_подтверждения',
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

        df.to_excel(f'Полный отчет посещаемости {name_event}.xlsx',index=False)
        short_df.to_excel(f'Краткий отчет посещаемости {name_event}.xlsx',index=False)

        with open(f'Полный отчет посещаемости {name_event}.xlsx','rb') as file:
            await bot.send_document(message.from_user.id,file)

        with open(f'Краткий отчет посещаемости {name_event}.xlsx','rb') as file1:
            await bot.send_document(message.from_user.id,file1)

        # выходим из машины состояния
        await state.finish()
        await bot.send_message(message.from_user.id,'Скачайте нужный файл',reply_markup=keyboards.admin_kb.kb_admin_course)

# Обработка события редактирования курса
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit '))
async def get_edit_course_callback_run(callback_query: types.CallbackQuery,state=FSMContext):
    # Получаем айди нужного курса
    id_course = callback_query.data.replace('edit ', '')
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if callback_query.from_user.id == ID:
        # Переводим машину состояний в первую стадию загрузка айди курса
        await FSMEditCourseAdmin.id_course.set()
        async with state.proxy() as data:
            data['id_course'] = id_course
        await FSMEditCourseAdmin.next()
        # Пишем сообщение пользователю, что ему нужно загрузить фото
        await callback_query.message.reply('Загрузите фото курса\nЧтобы прекратить редактирование напишите в чат слово стоп')


async def edit_photo_course(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Через контекстный менеджер получаем записываем в словарь  айди загруженной картинки
            data['img_course'] = message.photo[0].file_id
            # Переводим машину состояний в следующую фазу
        await FSMEditCourseAdmin.next()
        # Сообщаем пользователю что нужно ввести название курса
        await message.reply('Введите название курса\nЧтобы прекратить редактирование напишите в чат слово стоп')

async def edit_name_course(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        # К Через контекстный менеджер записываем с словарь название курса
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['name_course'] = message.text
        await FSMEditCourseAdmin.next()
        # Сообщаем пользователю что нужно ввести описание курса
        await message.reply('Введите описание курса\nЧтобы прекратить редактирование напишите в чат слово стоп')


async def edit_description_course(message: types.Message, state: FSMContext):
    # К Через контекстный менеджер записываем в словарь описание курса
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['description_course'] = message.text
        await FSMEditCourseAdmin.next()
        # Сообщаем пользователю что нужно ввести сведения о том кто может записаться и как записаться
        await message.reply('Введите кто,как и на каких условиях может записаться на курс\nЧтобы прекратить загрузку напишите в чат слово стоп')

async def edit_how_sign_course(message: types.Message, state: FSMContext):
    # К Через контекстный менеджер записываем в словарь как записаться на курс
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['how_sign_course'] = message.text
        # Переводим машину в следующее состояние
        await FSMEditCourseAdmin.next()
        # Сообщаем пользователю что нужно ввести сведения о типе мероприятия
        await message.reply('Введите да, если это событие\nВведите нет,если это обычный курс\nЧтобы прекратить загрузку напишите в чат слово стоп')

async def edit_event_mark_course(message:types.Message,state: FSMContext):
    # К Через контекстный менеджер записываем в словарь является ли курс мероприятием
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        check_message_text = message.text.lower()
        # проверка правильности ввода
        if check_message_text == 'да' or check_message_text == 'нет':
            async with state.proxy() as data:
                data['event_mark'] = check_message_text
            await FSMEditCourseAdmin.next()
            await message.reply(
                'Введите да, чтобы сделать курс видимым\nВведите нет,если чтобы скрыть курс\nЧтобы прекратить загрузку напишите в чат слово стоп')

        else:
            await message.reply('Введите да, если это событие\nВведите нет,если это обычный курс')

async def edit_event_visible_course(message:types.Message,state: FSMContext):
    # К Через контекстный менеджер записываем в словарь является ли курс мероприятием
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        check_message_text = message.text.lower()
        # проверка правильности ввода
        if check_message_text == 'да' or check_message_text == 'нет':
            async with state.proxy() as data:
                data['visible'] = check_message_text
            await sqlite_db.sql_update_course(state)
            await message.answer('Данные курса(мероприятия) отредактированы!')
            await state.finish()
        else:
            await message.reply('Введите да, чтобы сделать курс видимым\nВведите нет,если чтобы скрыть курс\nЧтобы прекратить загрузку напишите в чат слово стоп')

async def load_news(message:types.Message):
    """
    Функция для начала загрузки новости.Старт машины состояний
    """
    if message.from_user.id == ID:
        # Переводим машину состояний в первую стадию загрузка фото курса
        await FSMLoadNews.img_news.set()
        # Пишем сообщение пользователю, что ему нужно загрузить фото
        await message.reply('Загрузите фото новости\nЧтобы прекратить загрузку напишите в чат слово стоп')


async def load_img_news(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Через контекстный менеджер получаем записываем в словарь  айди загруженной картинки
            data['img_news'] = message.photo[0].file_id
            # Переводим машину состояний в следующую фазу
        await FSMLoadNews.next()
        # Сообщаем пользователю что нужно ввести название курса
        await message.reply('Введите краткое описание новости вместе с ссылкой на исходный сайт\nЧтобы прекратить загрузку напишите в чат слово стоп')

async def load_description_news(message:types.Message,state: FSMContext):

    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description_news'] = message.text
            data['date_news'] = message.date
        await sqlite_db.sql_add_news(state)
        await message.answer('Новость добавлена!')
        await state.finish()

async def edit_news(message:types.Message):
    """
    Функция для запуска обработки новостей
    """
    if message.from_user.id == ID:
        # Получаем из таблицы данные новости. Так для пользователя отображется последние 3 новости, то и редактировать имеет смысл только те новости
        # которые показываются пользователю
        news = await sqlite_db.sql_read_news()

        for row in news:
            #Создаем клавиатуру
            inline_kb_admin_news = InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'Редактировать новость', callback_data=f'edit_news {row[0]} ')).add(
                InlineKeyboardButton(f'Удалить новость', callback_data=f'del_news {row[0]}'))
            # Отправляем список новостей
            await bot.send_message(message.from_user.id,f'{row[2]}')
            await bot.send_message(message.from_user.id,text='Нажмите нужную кнопку',
                                   reply_markup=inline_kb_admin_news)

#Обработчик для удаления новостей
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del_news'))
async def delete_news_callback_run(callback_query: types.CallbackQuery):
    """
    Функция для удаления новости
    """

    # если проверка на флуд пройдена то начинаем работу
    # Получаем айди нужного мероприятия
    id_news = callback_query.data.replace('del_news ', '')
    await sqlite_db.sql_delete_news(id_news)
    await bot.send_message(callback_query.from_user.id, f'Новость удалена!')
    await callback_query.answer('Новость удалена', show_alert=True)

# Обработчик для редактирования новостей
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit_news'))
async def edit_news_callback_run(callback_query: types.CallbackQuery,state=FSMContext):
    # Получаем айди нужной новости
    id_news = callback_query.data.replace('edit_news ', '')
    if callback_query.from_user.id == ID:
        # Переводим машину состояний в первую стадию загрузка айди новости
        await FSMEditNews.id_news.set()
        async with state.proxy() as data:
            data['news_id'] = id_news
        await FSMEditNews.next()
        await callback_query.message.reply(
            'Загрузите фото новости\nЧтобы прекратить редактирование напишите в чат слово стоп')

async def edit_photo_news(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Через контекстный менеджер получаем записываем в словарь  айди загруженной картинки
            data['img_news'] = message.photo[0].file_id
            # Переводим машину состояний в следующую фазу
        await FSMEditNews.next()
        # Сообщаем пользователю что нужно ввести название курса
        await message.reply('Введите краткое описание новости вместе с ссылкой на исходный сайт\nЧтобы прекратить редактирование напишите в чат слово стоп')

async def edit_description_news(message:types.Message,state:FSMContext):
    """
    Функция для редактирования описания новости
    """
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description_news'] = message.text
            data['date_news'] = message.date
        # Отправляем запрос в базу данных
        await sqlite_db.sql_edit_news(state)
        await message.answer('Новость отредактирована!')
        await state.finish()




async def general_report(message:types.Message):
    """
    Функция для получения общей таблицы курсов и общей таблицы заявок
    """
    all_courses = await sqlite_db.sql_read_all_courses()
    df_courses = pd.DataFrame(all_courses,columns=['ID_курса','Картинка курса','Название курса','Описание курса','Как записаться','Событие да/нет','Видимость в каталоге да/нет'])


    all_app = await sqlite_db.sql_read_all_app()
    df_app = pd.DataFrame(all_app, columns=['ID_заявки', 'ID_курса', 'ID_участника', 'Телефон', 'Имя', 'Фамилия','Время регистрации'
        , 'Широта геометки пользователя', 'Долгота геометки пользователя', 'Время подтверждения присутствия'])

    # Приводим к одному типу данных колонку ID курса чтобы слияние прошло корректно
    df_courses['ID_курса'] = df_courses['ID_курса'].astype(int)
    df_app['ID_курса'] = df_app['ID_курса'].astype(int)
    # мержим 2 датафрейма чтобы в вместо айди курса показывалось его название

    named_course_df = df_app.merge(df_courses,how='inner',left_on='ID_курса',right_on='ID_курса')
    # Удаляем лишние колонки
    named_course_df.drop(columns=['Картинка курса','Описание курса','Как записаться','Событие да/нет','Видимость в каталоге да/нет'],inplace=True)
    # Меняем порядок колонок
    named_course_df = named_course_df.reindex(columns=['ID_заявки','Название курса','ID_курса','Телефон', 'Имя', 'Фамилия','Время регистрации'
        , 'Широта геометки пользователя', 'Долгота геометки пользователя', 'Время подтверждения присутствия'])

    # Сохраняем датафреймы
    # Получаем текущее время для того чтобы использовать в названии
    t = time.localtime()
    current_time = time.strftime('%H_%M_%S', t)
    df_courses.to_excel(f'Список курсов ЦОПП {current_time}.xlsx',index=False)
    named_course_df.to_excel(f'Общий список заявок на курсы ЦОПП {current_time}.xlsx',index=False)

    # Отправляем полученные файлы в чат
    with open(f'Список курсов ЦОПП {current_time}.xlsx', 'rb') as file_courses:
        await bot.send_document(message.from_user.id, file_courses)
    with open(f'Общий список заявок на курсы ЦОПП {current_time}.xlsx', 'rb') as file_app:
        await bot.send_document(message.from_user.id, file_app)






# регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(load_course, commands='Загрузить', state=None)
    # dp.register_message_handler(cancel_handler_load_course, state="*", commands='отмена')
    dp.register_message_handler(admin_cancel_handler_load_course,Text(equals='стоп', ignore_case=True), state="*")
    # Хэндлеры машины состояний загрузки курсов
    dp.register_message_handler(load_photo_course, content_types=['photo'], state=FSMAdmin.photo_course)
    dp.register_message_handler(load_name_course, state=FSMAdmin.name_course)
    dp.register_message_handler(load_description_course, state=FSMAdmin.description_course)
    dp.register_message_handler(load_how_sign_course, state=FSMAdmin.how_sign_course)
    dp.register_message_handler(load_event_mark_course,state=FSMAdmin.event_mark)
    dp.register_message_handler(load_event_visible_course,state=FSMAdmin.visible)
    # Хэндлеры машины состояний посещаемости
    dp.register_message_handler(get_confirmed_callback_run,state=FSMReportAdmin.name_event)
    dp.register_message_handler(set_event_location,content_types=['location'],state=FSMReportAdmin.event_location)
    dp.register_message_handler(set_time_begin_event,state=FSMReportAdmin.time_begin_event)
    dp.register_message_handler(set_time_end_event,state=FSMReportAdmin.time_end_event)
    dp.register_message_handler(set_distance_event,state=FSMReportAdmin.distance_event)
    dp.register_message_handler(processing_report_participants,state=FSMReportAdmin.create_report)
    dp.register_message_handler(dysplay_course, commands=['Редактировать'])
    dp.register_message_handler(report_event,commands=['Отчетность'])
    # Хэндлеры машины состояний редактирования курсов
    dp.register_message_handler(edit_photo_course, content_types=['photo'], state=FSMEditCourseAdmin.photo_course)
    dp.register_message_handler(edit_name_course,state=FSMEditCourseAdmin.name_course)
    dp.register_message_handler(edit_description_course,state=FSMEditCourseAdmin.description_course)
    dp.register_message_handler(edit_how_sign_course,state=FSMEditCourseAdmin.how_sign_course)
    dp.register_message_handler(edit_event_mark_course,state=FSMEditCourseAdmin.event_mark)
    dp.register_message_handler(edit_event_visible_course,state=FSMEditCourseAdmin.visible)

    # Хэндлеры машины состояний создания новости
    dp.register_message_handler(load_news,commands=['Создать_новость'])
    dp.register_message_handler(load_img_news, content_types=['photo'], state=FSMLoadNews.img_news)
    dp.register_message_handler(load_description_news, state=FSMLoadNews.description_news)

    # Хэндлеры редактирования новостей
    dp.register_message_handler(edit_news,commands=['Редактировать_новости'])
    dp.register_message_handler(edit_photo_news,content_types=['photo'],state=FSMEditNews.img_news)
    dp.register_message_handler(edit_description_news,state=FSMEditNews.description_news)


    dp.register_message_handler(general_report,commands=['Общая_отчетность'])

    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)
