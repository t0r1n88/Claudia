:: Отключаем вывод служебной информации
@echo off
::Активируем виртуальное окружение
call %~dp0venv\Scripts\activate


:: Создаем переменную среды окружения
set TOKEN=5549256746:AAHQ8_nqbihLpEkVN20zNro4I92c_JUr_9k

::Запускаем скрипт
python application_to_study_telegram_bot.py

:: Чтобы при ошибке окно не закрывалось и можно было увидет ошибку
pause

