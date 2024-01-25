# tg-web-client
Это не бот. Это клиент для телеграм. Точнее стартовый каркас.
Использовано: thelethon, asyncio, pydantic, poetry

## Запуск

git pull
python -m venv .venv
python . ./.venv/bin/activate
pip install --upgrade pip poetry
poetry install

Необходимо вставить свои данные в строки 
TELEGRAM_API_ID = 10042
TELEGRAM_API_HASH = "46d123321325f70b93e7ba"

python src/main.py
