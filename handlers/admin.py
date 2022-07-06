from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создаем константу
ID = None


class FSMAdmin(StatesGroup):
    """
    Класс в котором мы создаем состояния для шагов машины состояний
    """
    # Состояния которые будут использоватья в процессе загрузки нового курса
    photo_course = State()
    name_course = State()
    description_course = State()
    how_sign_course = State()


# проверяем пользователя на права администратора в группе
# @dp.message_handler(commands=['admin'],is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    # Получаем айди пользователя
    ID = message.from_user.id
    # Отправляем сообщение через бота в личку пользователю
    await bot.send_message(message.from_user.id, 'Что прикажете повелитель?', reply_markup=admin_kb.kb_admin_course)
    await message.delete()


# Начало диалога загрузки нового курса
# Для начала работы требуем прописать команду Загрузить. состояние машины состояний(ха) инициаизируется None
# @dp.message_handler(commands='Загрузить',state=None)
async def load_course(message: types.Message):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        # Переводим машину состояний в первую стадию загрузка фото курса
        await FSMAdmin.photo_course.set()
        # Пишем сообщение пользователю, что ему нужно загрузить фото
        await message.reply('Загрузите фото курса')


# Добавляем обязательную кнопку для выхода из машины состояний
# "*" означает любое состояние машины состояний
# 2 декоратора нужны чтобы можно было отменить как прописав команду через \ так и просто написав слово отмена
# @dp.message_handler(state="*",commands='отмена')
# @dp.message_handler(Text(equals='отмена',ignore_case=True),state="*")
async def cancel_handler_load_course(message: types.Message, state: FSMContext):
    # получаем текущее состояние машины состояний
    current_state = await state.get_state()
    # Если машина не находится в каком либо состоянии то ничего не делаем, в противном случае завершаем машину состояний
    if current_state is None:
        return
    await state.finish()
    await message.reply('Загрузка курса отменена')


# получаем ответ пользователя и записываем в словарь
# ограничиваем загрузку только фото и указываем что машина состояний должна находиться в стадии photo_course
# @dp.message_handler(content_types=['photo'],state=FSMAdmin.photo_course)
async def load_photo_course(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Через контекстный менеджер получаем записываем в словарь  айди загруженной картинки
            data['img_course'] = message.photo[0].file_id
            # Переводим машину состояний в следующую фазу
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести название курса
        await message.reply('Введите название курса')


# Получаем от пользователя название курса
# @dp.message_handler(state=FSMAdmin.name_course)
async def load_name_course(message: types.Message, state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        # К Через контекстный менеджер записываем с словарь название курса
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['name_course'] = message.text
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести описание курса
        await message.reply('Введите описание курса')


# Получаем от пользователя описание курса
# @dp.message_handler(state=FSMAdmin.description_course)
async def load_description_course(message: types.Message, state: FSMContext):
    # К Через контекстный менеджер записываем в словарь описание курса
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['description_course'] = message.text
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести сведения о том кто может записаться и как записаться
        await message.reply('Введите кто,как и на каких условиях может записаться на курс')


# Получаем от пользователя описание того как записаться на курс
# @dp.message_handler(state=FSMAdmin.how_sign_course)
async def load_how_sign_course(message: types.Message, state: FSMContext):
    # К Через контекстный менеджер записываем в словарь как записаться на курс
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['how_sign_course'] = message.text
        # Заканчиваем переходы по состояниям
        # После выполнения этой команды словарь data очищается.Поэтому нужно сохранить данные
        await sqlite_db.sql_add_course(state)
        await message.answer('Данные курса добавлены')

        await state.finish()


# Декоратор для ответа на  команду на удаление. Т.е если запрос будет не пустой и он будет начинаться с del то функция выполнится
# Более понятное объяснение https://youtu.be/gpCIfQUbYlY?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_course_callback_run(callback_query: types.CallbackQuery):
    # Получаем название курса который нужно удалить. в строке кроме названия есть еще del и поэтому очищаем строку
    deleted_course = callback_query.data.replace('del ', '')
    # Отправляем строку вида del название курса в функцию для удаления из базы данных.Передтэтим очищаем от del
    await sqlite_db.sql_delete_course(deleted_course)
    await callback_query.answer(f'Курс {deleted_course} удален', show_alert=True)


async def delete_course(message: types.Message):
    """
    Функция для удаления курса из базы данных
    """
    if message.from_user.id == ID:
        # Получаем из таблицы данные всех курсов
        all_course_data = await sqlite_db.sql_read_all_courses()
        # Итерируемся по полученному списку кортежей
        for course in all_course_data:
            # Создаем инлайн кнопку
            # inline_del_course_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}'))
            # Отправляем данные курса из таблицы
            await bot.send_photo(message.from_user.id, course[0],
                                 f'{course[1]}\nОписание курса: {course[2]}\n Условия записи на курс: {course[3]}')
            # Отправляем инлайн кнопку вместе с сообщением
            # await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}')))
            await bot.send_message(message.from_user.id, text='^^^',reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {course[1]}', callback_data=f'del {course[1]}')))


# регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(load_course, commands='Загрузить', state=None)
    dp.register_message_handler(cancel_handler_load_course, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler_load_course, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo_course, content_types=['photo'], state=FSMAdmin.photo_course)
    dp.register_message_handler(load_name_course, state=FSMAdmin.name_course)
    dp.register_message_handler(load_description_course, state=FSMAdmin.description_course)
    dp.register_message_handler(load_how_sign_course, state=FSMAdmin.how_sign_course)
    dp.register_message_handler(delete_course, commands=['Удалить'])
    dp.register_message_handler(make_changes_command, commands=['admin'], is_chat_admin=True)