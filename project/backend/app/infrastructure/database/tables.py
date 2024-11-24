from .db_connection import get_db_connection


async def create_products_table():
    """
    Ürünler için tabloyu oluştur.
    """
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        try:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description TEXT,
                    price NUMERIC NOT NULL,
                    photos JSONB
                );
            """)
            print("Products table checked/created successfully.")
        except Exception as e:
            print(f"Error creating products table: {e}")
            raise
