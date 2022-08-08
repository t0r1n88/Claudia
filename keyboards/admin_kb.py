# Кнопки клавиатуры админа
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем кнопки
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Редактировать')
button_stat = KeyboardButton('/Отчетность')
btn_stop = KeyboardButton('/Стоп')
btn_skip = KeyboardButton('/Пропустить')

# Создаем клавиатуру основного меню администратора
kb_admin_course = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete).add(button_stat)

# Создаем клавиатуру меню редактирования курсов
kb_admin_edit_course = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_skip).add(btn_stop)

# Создаем клавиатуру отправки локации

btn_share_location = KeyboardButton('Отправить локацию мероприятия', request_location=True)
kb_admin_event_location = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
kb_admin_event_location.add(btn_share_location)

