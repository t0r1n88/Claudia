from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

# Создаем кнопки
b1 = KeyboardButton('/Контакты')
b2 = KeyboardButton('/Режим_работы')
# Кнопки исключения потому что текст кнопок может быть любой, то есть не соответствовать команде
# Отправляет боту ваш телефон
b3 = KeyboardButton('Поделиться номером',request_contact=True)
# Отправляет боту ваше местоположение
b4 = KeyboardButton('Отправить где я',request_location=True)
b5 = KeyboardButton('/Текущие_курсы')
# Создаем клавиатуру
#one_time_keyboard=True аргумент овечающий за то что полсе использования клавиатура исчезает.Ее можно повторно вызвать нажав иконку
kb_client = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
# Добавление кнопок в стобец
# kb_client.add(b1).add(b2)
# #Добавление кнопки
# kb_client.add(b1).insert(b2)
#Кнопки в строку
kb_client.add(b1).add(b2).row(b3,b4).add(b5)


