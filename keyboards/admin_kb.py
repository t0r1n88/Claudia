# Кнопки клавиатуры админа
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# Создаем кнопки
btn_load_course = KeyboardButton('/Загрузить')
btn_edit_course = KeyboardButton('/Редактировать')
btn_create_news = KeyboardButton('/Создать_новость')
btn_edit_news = KeyboardButton('/Редактировать_новости')
btn_stat = KeyboardButton('/Отчетность')
btn_stop = KeyboardButton('/Стоп')
btb_general_report = KeyboardButton('/Общая_отчетность')

# Создаем клавиатуру основного меню администратора
kb_admin_course = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_load_course).add(btn_edit_course).add(btn_create_news).add(btn_edit_news).add(btn_stat).add(btb_general_report)


# Создаем клавиатуру отправки локации

btn_share_location = KeyboardButton('Отправить локацию мероприятия', request_location=True)
kb_admin_event_location = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
kb_admin_event_location.add(btn_share_location)




