from aiogram import types,Dispatcher
from create_bot import dp
import json, string


# @dp.message_handler()
async def main_handler(message: types.Message):
    # проверяем сообщение на мат. С помощью пересечения с множеством матов
    # ссылка на объяснение конструкции https://youtu.be/Lgm7pxlr7F0?list=PLNi5HdK6QEmX1OpHj0wvf8Z28NYoV5sBJ
    if {word.lower().translate(str.maketrans('', '', string.punctuation)) for word in
        message.text.split()}.intersection(set(json.load(open('cenz.json')))):
        await message.reply('Маты запрещены! Просим проявить уважение!!!')
        await message.delete()

def register_handlers_other(dp :Dispatcher):
    """
    Регистрируем хэндлеры клиента чтобы не писать над каждой функцией декоратор с командами
    """
    dp.register_message_handler(main_handler)