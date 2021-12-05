import databases

from .. import database


async def check_db_connected():
    try:
        db = databases.Database(database.SQLALCHEMY_DATABASE_URL)
        if not db.is_connected:
            await db.connect()
            await db.execute("SELECT 1")
        print("Database is connected.")
    except Exception as err:
        print("db is missing or there is some problem in connection")
        raise err


async def check_db_disconnected():
    try:
        db = databases.Database(database.SQLALCHEMY_DATABASE_URL)
        if db.is_connected:
            await db.disconnect()
        print("Database is Disconnected.")
    except Exception as err:
        raise err
