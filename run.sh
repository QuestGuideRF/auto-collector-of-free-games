#!/бин/баш
cd "$(имя каталога "$0")"
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python main.py
read -p "Нажмите Enter для выхода..."