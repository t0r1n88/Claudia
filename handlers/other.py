from aiogram import types,Dispatcher
from create_bot import dp
import json, string


# @dp.message_handler()
async def main_handler(message: types.Message):
    await message.delete()
    await message.answer('Используйте для работы кнопки внизу вашего экрана.')
    # await message.delete()
    # await message.answer('Для получения информации и записи на курсы, напишите  боту\nhttps://t.me/Application_to_COPP_BOT')





def register_handlers_other(dp :Dispatcher):
    """
    Регистрируем хэндлеры клиента чтобы не писать над каждой функцией декоратор с командами
    """
    dp.register_message_handler(main_handler,content_types=['text','audio','video','document','sticker','photo'])