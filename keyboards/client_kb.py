from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

# Создаем кнопки
btn_contacts_copp = KeyboardButton('/Контакты')
btn_work_regime = KeyboardButton('/Режим_работы')
# Кнопки исключения потому что текст кнопок может быть любой, то есть не соответствовать команде
# Отправляет боту ваш телефон
btn_share_contact = KeyboardButton('Поделиться номером', request_contact=True)
# Отправляет боту ваше местоположение
btn_share_location = KeyboardButton('Отправить где я', request_location=True)
current_courses = KeyboardButton('/Текущие_курсы')
# Создаем клавиатуру
#one_time_keyboard=True аргумент овечающий за то что полсе использования клавиатура исчезает.Ее можно повторно вызвать нажав иконку
kb_client = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
# Добавление кнопок в стобец
# kb_client.add(b1).add(b2)
# #Добавление кнопки
# kb_client.add(b1).insert(b2)
#Кнопки в строку
kb_client.add(btn_contacts_copp).add(btn_work_regime).row(btn_share_contact, btn_share_location).add(current_courses)

# Создаем клавиатуру для отправки своего контакта

kb_client_reg = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
kb_client_reg.add(btn_share_contact)



