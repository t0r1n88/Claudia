# импортируем excecutor для запуска бота в онлайн
from aiogram.utils import executor
from create_bot import dp
from handlers import client,admin,other


async def on_startup(_):
    """
    Функция выполняющая при старте бота, для подключения к базе данных

    """
    print('Бот вышел в онлайн')

# Запускаем функции из модулей client,admin,other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

# Запускаем бота
# skip_updates=True - для того чтобы бот не отвечал на сообщение пришедшие когда он бы не в онлайн
executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
