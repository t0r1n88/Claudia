# Кнопки клавиатуры админа
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем кнопки
button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Удалить')

# Создаем клавиатуру
kb_admin_course = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)