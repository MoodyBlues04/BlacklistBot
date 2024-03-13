import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_URI = os.getenv("DB_URI")
