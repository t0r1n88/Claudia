import sqlite3 as sq
from create_bot import bot

import pandas as pd
from io import BytesIO


# Создаем функцию для старта базы данных
def sql_start():
    global base, cur
    # Подключаемся к базе данных.Если такой базы нет  то создаем Бд с таким названием
    base = sq.connect('copp.db')
    # Создаем объект для управления базой данных
    cur = base.cursor()
    # Выводим сообщение в терминал если все прошло хорошо и к базе удалось подключитья
    if base:
        print('Подключение к таблице курсов ЦОПП произошло успешно!')
    else:
        print('Возникла проблема с подключением!!!')
    # Создаем таблицу если такой таблицы еще нет в базе данных
    # not EXISTS если таблица уже существует то ничего не делаем
    # img картинку мы храним в виде file.id хранимого на серверах телеграмма
    base.execute(
        'CREATE TABLE IF NOT EXISTS courses(course_id INTEGER PRIMARY KEY AUTOINCREMENT, img TEXT,'
        ' name_course TEXT, description_course TEXT, how_sign_course TEXT, event_mark TEXT,visible TEXT)')
    # Сохраняем эти изменения
    base.commit()
    # Создаем таблицу по учету участников мероприятия если ее нет
    base.execute(
        'CREATE TABLE IF NOT EXISTS participants(app_id INTEGER PRIMARY KEY, course_id TEXT, id_participant TEXT,'
        'phone TEXT, first_name TEXT, last_name TEXT,latitude TEXT, longitude TEXT,time_mark TEXT)')

    base.commit()


# Создаем функцию для добавления курса
async def sql_add_course(state):
    """
    Функция для добавления в базу данных содержимого словаря машины состояний
    :param state:машина состояний
    """
    async with state.proxy() as data:
        # Вставляем данные в таблицу
        cur.execute(
            'INSERT INTO courses(img,name_course,description_course,how_sign_course,event_mark,visible) VALUES (?,?,?,?,?,?)',
            tuple(data.values()))
        base.commit()

async def sql_check_exists_app(course_id,id_user):
    """
    Функция для проверки наличия записи в таблице
    """
    return cur.execute('SELECT app_id from participants WHERE course_id == ? AND id_participant == ?',(course_id,id_user)).fetchone()



async def sql_add_reg_on_event(state):
    """
    Функция для добавления в базу данных заявки на мероприятие
    """
    async with state.proxy() as data:
        # Вставляем данные в таблицу
        cur.execute('INSERT INTO participants(course_id,id_participant,phone,first_name,last_name) VALUES (?,?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_confirm_presense_on_location(state):
    """
    Функция для вставки значений геолокации в таблицу
    """
    async with state.proxy() as data:
        # Получаем кортеж
        temp_loc_data = tuple(data.values())
        """
        Порядок данных course_id,id_participant,latitude,longitude,event_mark
        """
    cur.execute(
        'UPDATE participants SET latitude == ?,longitude == ?, time_mark == ?  WHERE course_id == ? and id_participant == ?',
        [temp_loc_data[2], temp_loc_data[3], temp_loc_data[4], temp_loc_data[0], temp_loc_data[1]])
    base.commit()


# async def sql_read_course(message):
#     # Получаем все данные из таблицы Курсы в виде списка списков
#     return cur.execute('SELECT * FROM courses').fetchall()

async def sql_read_all_courses():
    """
    Функция для получени из базы данных всех текущих курсов
    """
    return cur.execute('SELECT * FROM courses').fetchall()


async def sql_read_name_course(id_course):
    """
    Функция для получения названия курса по айди курса
    """
    return cur.execute('SELECT name_course FROM courses WHERE course_id == ?', (id_course,)).fetchone()


async def sql_get_registered(course_id):
    """
    Функция для получения списка зарегистрировавшихся на мероприятие
    """
    # подключаемся к базе данных
    con = sq.connect('copp.db')
    # Считываем данные
    df = pd.read_sql("SELECT * FROM participants", con, parse_dates={'time_mark': {'errors': 'coerce'}})
    # Получаем записи относящиеся к нужному мероприятию
    selection_df = df[df['course_id'] == course_id]
    # Отбираем нужные колонки
    registered_df = selection_df[['app_id', 'course_id', 'id_participant', 'phone', 'first_name', 'last_name']].copy()

    # Делаем запрос чтобы получить название мероприятия распаковывая полученный кортеж
    tuple_name_event = await (sql_read_name_course(course_id))
    # Распаковываем кортеж
    name_event = tuple_name_event[0]
    # Присваиваем колонке course_id значение названия мероприятия
    registered_df['course_id'] = name_event
    # Переименовываем колонки
    registered_df.columns = ['ID заявки', 'Название мероприятия', 'Telegram ID пользователя', 'Телефон', 'Имя',
                             'Фамилия']
    # На будущее чтобы попробовать избежать сохранения на диске.
    # # Превращаем в объект Excel
    # bio = BytesIO()
    #
    # # By setting the 'engine' in the ExcelWriter constructor.
    # writer = pd.ExcelWriter(bio, engine="openpyxl")
    # registered_df.to_excel(writer, sheet_name="Sheet1")
    #
    # # Save the workbook
    # writer.save()
    #
    # # Seek to the beginning and read to copy the workbook to a variable in memory
    # bio.seek(0)
    # workbook = bio.read()
    #
    # return workbook
    # Поменять название мероприятия
    registered_df.to_excel(f'Список зарегистрировашихся на {name_event}.xlsx', index=False)

async def sql_get_confirmed(course_id):
    """
    Функция для получения заявок на определенное мероприятияе
    """
    return cur.execute('SELECT * FROM participants WHERE course_id == ?', (course_id,)).fetchall()

async def sql_delete_course(id_course):
    """
    Функция для удаления курса из базы данных
    """
    cur.execute('DELETE FROM courses WHERE course_id == ?', (id_course,))
    base.commit()

async def sql_cancel_reg_event(course_id,id_participant):
    """
    Функция для отмены записи участника на мероприятие
    """
    cur.execute('DELETE FROM participants WHERE course_id == ? AND id_participant == ?', (course_id,id_participant))
    base.commit()

async def sql_check_exist_course(course_id):
    """
    Функция для проверки существования курса. Поскольку курс может быть удален
    """
    return cur.execute('SELECT course_id FROM courses WHERE course_id == ?',(course_id,)).fetchone()