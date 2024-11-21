import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "products",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def get_product_from_db(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cur.fetchone()
    conn.close()
    return product

def save_product_to_db(product):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO products (id, name, description, price, photos)
        VALUES (%s, %s, %s, %s, %s)
    """, (product["id"], product["name"], product["description"], product["price"], product["photos"]))
    conn.commit()
    conn.close()