import sqlite3

from app.shared.config import settings

def db_wrapper(func):
    async def wrapper(*args, **kwargs):
        conn = sqlite3.connect(settings.database_name)
        try:
            cursor = conn.cursor()
            result = await func(*args, **kwargs, cursor=cursor)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    return wrapper
