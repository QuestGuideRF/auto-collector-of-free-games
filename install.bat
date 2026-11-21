@echo off
chcp 65001 > nul
echo ============================================
echo   Установка Auto-collector of free games
echo ============================================
echo.
echo [1/4] Создание виртуального окружения...
python -m venv venv
if errorlevel 1 (
    echo ОШИБКА: Не удалось создать виртуальное окружение
    echo Убедитесь, что Python 3.8+ установлен и добавлен в PATH
    pause
    exit /b 1
)
echo [2/4] Активация виртуального окружения...
call venv\Scripts\activate.bat
echo [3/4] Установка зависимостей...
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)
echo [4/4] Создание конфигурационного файла...
if not exist "config.json" (
    copy config.json.example config.json
    echo Файл config.json создан
) else (
    echo Файл config.json уже существует
)
echo.
echo ============================================
echo   Установка завершена успешно!
echo ============================================
echo.
echo Следующие шаги:
echo 1. Откройте config.json и заполните данные для входа
echo 2. Запустите run.bat для однократной проверки
echo 3. Запустите run_scheduled.bat для работы по расписанию
echo.
pause