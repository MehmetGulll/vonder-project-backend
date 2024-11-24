import asyncpg

DB_CONFIG = {
    "user": "postgres",
    "password": "password",
    "database": "products",
    "host": "postgres",
    "port": 5432
}

pool = None


async def get_db_connection():
    """
    Veritabanı bağlantı havuzunu döndür.
    """
    global pool
    if not pool:
        pool = await asyncpg.create_pool(**DB_CONFIG)
    return pool
