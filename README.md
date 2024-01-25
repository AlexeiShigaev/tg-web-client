# tg-web-client
Это не бот. Это клиент телеграм. Точнее стартовый каркас.
Использовано: thelethon, asyncio, pydantic, poetry

## В общих словах
После запуска, открываем в браузере страницу http://localhost:8899. 
Для авторизации указываем номер телефона. Будет предъявлен QR-code. 
В смартфоне в телеграм идем в Настройки/Устройства/Подключить устройство.

После авторизации загрузится клиентская страница, список контактов и последние 10 сообщений для каждого из них.

## Запуск

```
git pull
python -m venv .venv
python . ./.venv/bin/activate
pip install --upgrade pip poetry
poetry install
```

Необходимо вставить свои данные в строки в mytelethon/src/api/tgclient.py
```
TELEGRAM_API_ID = 10042
TELEGRAM_API_HASH = "46d123321325f70b93e7ba"
```
далее
```
python src/main.py
```


