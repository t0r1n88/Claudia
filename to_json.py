"""
Скрипт для подготовки файла с фильтром мата
"""
import json
# пустой список куда будем добавлять слова
lst_swearing = []
# Открываем в контекстном менеджере файл
with open('Антимат.txt',encoding='utf-8') as file:
    for row in file:
        # Делим по знаку переноса и берем первый элемент
        value = row.lower().split('\n')[0]
        if value != '':
            lst_swearing.append(value)
# Записываем получившийся файл
with open('cenz.json','w',encoding='utf-8') as output_file:
    json.dump(lst_swearing,output_file)

