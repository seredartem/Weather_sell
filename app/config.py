import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_CONFIG = {
        "host": os.getenv("DB_DOMEN"),
        "port": int(os.getenv("DB_PORT")),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_LOGIN"),
        "pool_size": int(os.getenv("DB_POOL_SIZE")),
        "charset": os.getenv("DB_CHARSET"),
    }
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    KEY_WEATHER = os.getenv("KEY_WEATHER")