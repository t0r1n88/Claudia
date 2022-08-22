:: Отключаем вывод служебной информации
@echo off
::Активируем виртуальное окружение
call %~dp0venv\Scripts\activate


::Запускаем скрипт
python application_to_study_telegram_bot.py

:: Чтобы при ошибке окно не закрывалось и можно было увидет ошибку
pause

