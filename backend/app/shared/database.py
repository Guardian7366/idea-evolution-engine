import sqlite3

from app.shared.config import settings

def db_wrapper(func):
    async def wrapper(*args, **kwargs):
        # If cursor is already in kwargs, use it
        if "cursor" in kwargs:
            return await func(*args, **kwargs)
        else:
            try:
                # Otherwise, create a new cursor and pass it to the function
                conn = sqlite3.connect(settings.database_name)
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
