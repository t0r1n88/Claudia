from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

# Создаем кнопки
btn_contacts_copp = KeyboardButton('/Контакты')
btn_work_regime = KeyboardButton('/Режим_работы')
btn_current_courses = KeyboardButton('/На_что_можно_записаться')
btn_news = KeyboardButton('/Новости')
btn_main_menu = KeyboardButton('/Главное_меню')
btn_cancel = KeyboardButton('/Отмена')
# Кнопки исключения потому что текст кнопок может быть любой, то есть не соответствовать команде
# Отправляет боту ваш телефон
btn_share_contact = KeyboardButton('Поделиться номером', request_contact=True)
# Отправляет боту ваше местоположение
btn_share_location = KeyboardButton('Отправить где я', request_location=True)



# Создаем клавиатуру
#one_time_keyboard=True аргумент овечающий за то что полсе использования клавиатура исчезает.Ее можно повторно вызвать нажав иконку
kb_client = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)

# kb_client.row(btn_contacts_copp,btn_work_regime).add(current_courses)
kb_client.add(btn_current_courses).row(btn_contacts_copp,btn_work_regime).add(btn_news)

# Создаем клавиатуру для отправки своего контакта

kb_client_reg = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
kb_client_reg.add(btn_share_contact).add(btn_cancel).add(btn_main_menu)

kb_client_confirm_presense = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
kb_client_confirm_presense.add(btn_share_location).add(btn_cancel).add(btn_main_menu)

