import sqlite3 as sq
from create_bot import bot


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
        'CREATE TABLE IF NOT EXISTS courses(img TEXT, name_course TEXT PRIMARY KEY, description_course TEXT, how_sign_course TEXT)')
    # Сохраняем эти изменения
    base.commit()


# Создаем функцию для добавления курса
async def sql_add_course(state):
    """
    Функция для добавления в базу данных содержимого словаря машины состояний
    :param state:машина состояний
    """
    async with state.proxy() as data:
        # Вставляем данные в таблицу
        cur.execute('INSERT INTO courses VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read_course(message):
    # Получаем все данные из таблицы Курсы в виде списка списков
    for row in cur.execute('SELECT * FROM courses').fetchall():
        # Формируем сообщение пользователю. Отправляем данные из таблицы
        # row[0] это айди картинки на сервере телеграмма
        await bot.send_photo(message.from_user.id, row[0],f'{row[1]}\nОписание курса: {row[2]}\n Условия записи на курс: {row[3]}')

async def sql_read_all_courses():
    """
    Функция для получени из базы данных всех текущих курсов
    """
    return cur.execute('SELECT * FROM courses').fetchall()

async def sql_delete_course(name_course):
    """
    Функция для удаления курса из базы данных
    """
    cur.execute('DELETE FROM courses WHERE name_course == ?',(name_course,))
    base.commit()