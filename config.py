from dotenv import load_dotenv
import os
from json import loads

from vkbottle import API

from db_api.postgresql import Database

load_dotenv()

ADMINS = list(map(int, loads(os.getenv("ADMINS"))))
GROUP_ID = os.getenv("GROUP_ID")
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

api = API(token=BOT_TOKEN)

DB_USER = str(os.getenv("DB_USER"))
DB_PASS = str(os.getenv("DB_PASS"))
DB_NAME = str(os.getenv("DB_NAME"))
DB_HOST = str(os.getenv("DB_HOST"))

db = Database()
