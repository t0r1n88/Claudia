"""
Изучение sqllite3
"""
import sqlite3
# Коннектимся к базе данных, если такой базы нет то она создается
base = sqlite3.connect('new.db')
# Создаем курсор. Т.е. объект с помощью которого мы будем читать и изменять таблицы в базе данных
cur = base.cursor()
"""
не забьвать что у sqlite динамическая типизация, но при создании таблицы можно заранее прописывать типы
Всего их  5
text:str,integer:int,real:float,blob:любой тип данных,null:None

"""

# Создаем первую таблицу
base.execute('CREATE TABLE IF NOT EXISTS data(login,password text)')
# Сохраняем изменения
base.commit()

# Вставлем данные
# синтаксис (?,?) количечество вопросов равно количеству столбцов данных, нужен для того чтобы избежать SQL иньекций.
# cur.execute('INSERT INTO data VALUES(?, ?)',('t0r1n88','123456'))
# cur.execute('INSERT INTO data VALUES(?, ?)',('agronom','aedgd'))
# base.commit()

# Если нужно вставить много данных то нужно использовать executemany
# cur.executemany('INSERT INTO data VALUES(?, ?)',какие то данные которые автоматически распаковываются)

# Получаем данные
# fetchall() получить все значения.СОхраняем в переменную result
# result = cur.execute('SELECT * FROM data').fetchall()
# print(result)
# # Получаем данные по условию
# # Снова используем символ вопроса чтобы избежать иньекций. Значение по которому происходит отбор заключаем в кортеж
# result = cur.execute('SELECT password FROM data WHERE login==?',('t0r1n88',)).fetchone()
# print(result)
# Обновление поля таблицы
cur.execute('UPDATE data set password == ? WHERE login == ?',('Cassandra','t0r1n88'))
base.commit()
result = cur.execute('SELECT * FROM data').fetchall()
print(result)
# Удаляем значение
cur.execute('DELETE FROM data WHERE login == ?',('agronom',))
base.commit()

result = cur.execute('SELECT * FROM data').fetchall()
print(result)
# Удаление таблицы
base.execute('DROP TABLE IF EXISTS data')
base.commit()
# Отключаемся от базы данных
base.close()


