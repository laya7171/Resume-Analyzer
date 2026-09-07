import sqlite3
from app.config.core import settings


def get_connection():
    return sqlite3.connect(settings.database_path)