import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        total_amount REAL NOT NULL,
        order_date TIMESTAMP NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Non", 5000, "Non mahsulotlari"),
            ("Sut", 12000, "Sut mahsulotlari"),
            ("Go'sht", 85000, "Go'sht mahsulotlari"),
            ("Olma", 15000, "Mevalar"),
            ("Kartoshka", 8000, "Sabzavotlar"),
            ("Shokolad", 18000, "Shirinliklar"),
            ("Suv", 4000, "Ichimliklar"),
            ("Guruch", 14000, "Dukkon mahsulotlari"),
            ("Tuxum (10 dona)", 20000, "Oziq-ovqat"),
            ("Pishloq", 45000, "Sut mahsulotlari")
        ]

        insert_query = "INSERT INTO products (name, price, category) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, sample_products)

    conn.commit()
    conn.close()
