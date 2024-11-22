import asyncpg
import json

DB_CONFIG = {
    "user": "postgres",
    "password": "password",
    "database": "products",
    "host": "postgres",
    "port": 5432
}
pool = None
async def get_db_connection():
    global pool
    if not pool:
        pool = await asyncpg.create_pool(**DB_CONFIG)
    return pool

async def create_products_table():
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

async def async_get_product_from_db(product_id: str):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        query = "SELECT id, name, description, price, photos FROM products WHERE id = $1"
        product = await conn.fetchrow(query, product_id)
        if product:
            product_dict = dict(product)
            if isinstance(product_dict['photos'], str):
                product_dict['photos'] = json.loads(product_dict['photos'])  
            return product_dict
        return None



async def async_get_all_products(limit: int, offset: int):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        try:
            query = """
                SELECT id, name, description, price, photos
                FROM products
                ORDER BY name
                LIMIT $1 OFFSET $2
            """
            products = await conn.fetch(query, limit, offset)
            return [
                {
                    "id": product["id"],
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["price"],
                    "photos": json.loads(product["photos"]) if isinstance(product["photos"], str) else product["photos"],
                }
                for product in products
            ]
        except Exception as e:
            print(f"Error fetching products: {e}")
            raise




async def async_save_product_to_db(product: dict, vendor_name: str):
    pool = await get_db_connection()
    async with pool.acquire() as conn:
        try:
            unique_id = f"{vendor_name}-{product['id']}"
            photos_json = json.dumps(product["photos"]) 
            await conn.execute("""
                INSERT INTO products (id, name, description, price, photos)
                VALUES ($1, $2, $3, $4, $5::jsonb)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    price = EXCLUDED.price,
                    photos = EXCLUDED.photos
            """, unique_id, product["name"], product["description"],
                product["price"], photos_json)
        except Exception as e:
            print(f"Error saving product: {e}")
            raise
