#!/бин/баш
echo "============================================"
echo "  Установка Auto-collector of free games"
echo "============================================"
echo ""
echo "[1/4] Создание виртуального окружения..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось создать виртуальное окружение"
    echo "Убедитесь, что Python 3.8+ установлен"
    exit 1
fi
echo "[2/4] Активация виртуального окружения..."
source venv/bin/activate
echo "[3/4] Установка зависимостей..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить зависимости"
    exit 1
fi
echo "[4/4] Создание конфигурационного файла..."
if [ ! -f "config.json" ]; then
    cp config.json.example config.json
    echo "Файл config.json создан"
else
    echo "Файл config.json уже существует"
fi
echo ""
echo "============================================"
echo "  Установка завершена успешно!"
echo "============================================"
echo ""
echo "Следующие шаги:"
echo "1. Откройте config.json и заполните данные для входа"
echo "2. Запустите ./run.sh для однократной проверки"
echo "3. Запустите ./run_scheduled.sh для работы по расписанию"
echo ""
chmod +x run.sh
chmod +x run_scheduled.sh