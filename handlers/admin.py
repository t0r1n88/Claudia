from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from create_bot import dp,bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text

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
async def make_changes_command(message:types.Message):
    global ID
    # Получаем айди пользователя
    ID = message.from_user.id
    # Отправляем сообщение через бота в личку пользователю
    await bot.send_message(message.from_user.id, 'Что прикажете повелитель?')
    await message.delete()


# Начало диалога загрузки нового курса
# Для начала работы требуем прописать команду Загрузить. состояние машины состояний(ха) инициаизируется None
# @dp.message_handler(commands='Загрузить',state=None)
async def load_course(message:types.Message):
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
async def cancel_handler_load_course(message:types.Message,state:FSMContext):
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
async def load_photo_course(message:types.Message,state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Через контекстный менеджер получаем записываем в словарь  айди загруженной картинки
            data['photo_course'] = message.photo[0].file_id
            # Переводим машину состояний в следующую фазу
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести название курса
        await message.reply('Введите название курса')

# Получаем от пользователя название курса
# @dp.message_handler(state=FSMAdmin.name_course)
async def load_name_course(message:types.Message,state: FSMContext):
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
    #К Через контекстный менеджер записываем с словарь название курса
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['name_course'] = message.text
        await FSMAdmin.next()
        # Сообщаем пользователю что нужно ввести описание курса
        await message.reply('Введите описание курса')

# Получаем от пользователя описание курса
# @dp.message_handler(state=FSMAdmin.description_course)
async def load_description_course(message:types.Message,state:FSMContext):
    #К Через контекстный менеджер записываем в словарь описание курса
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
async def load_how_sign_course(message:types.Message,state:FSMContext):
    #К Через контекстный менеджер записываем в словарь как записаться на курс
    # Если айди пользователя равно айди полученному через функцию make_changes_command, то запускаем машину состояний
    if message.from_user.id == ID:
        async with state.proxy() as data:
            # Извлекаем из сообщения атрибут text
            data['how_sign_course'] = message.text
        # Заканчиваем переходы по состояниям
        # После выполнения этой команды словарь data очищается.Поэтому нужно сохранить данные
        async with state.proxy() as data:
            await message.reply(str(data))
        await state.finish()



# регистрируем хендлеры
def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(load_course,commands='Загрузить',state=None)
    dp.register_message_handler(load_photo_course,content_types=['photo'],state=FSMAdmin.photo_course)
    dp.register_message_handler(cancel_handler_load_course, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler_load_course, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_name_course,state=FSMAdmin.name_course)
    dp.register_message_handler(load_description_course,state=FSMAdmin.description_course)
    dp.register_message_handler(load_how_sign_course,state=FSMAdmin.how_sign_course)
    dp.register_message_handler(make_changes_command,commands=['admin'],is_chat_admin=True)








