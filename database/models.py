from database.db import get_connection
from datetime import datetime


class Product:
    @staticmethod
    def get_categories():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    @staticmethod
    def get_by_category(category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM products WHERE category = %s ORDER BY name", (category,))
        products = cursor.fetchall()
        conn.close()
        return products

    @staticmethod
    def get_by_id(product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, category FROM products WHERE id = %s", (product_id,))
        product = cursor.fetchone()
        conn.close()
        return product

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, category FROM products ORDER BY category, name")
        products = cursor.fetchall()
        conn.close()
        return products

    @staticmethod
    def add(name, price, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, category) VALUES (%s, %s, %s)",
                       (name, price, category))
        conn.commit()
        conn.close()

    @staticmethod
    def update(product_id, field, value):
        conn = get_connection()
        cursor = conn.cursor()

        if field == "name":
            cursor.execute("UPDATE products SET name = %s WHERE id = %s", (value, product_id))
        elif field == "price":
            cursor.execute("UPDATE products SET price = %s WHERE id = %s", (float(value), product_id))
        elif field == "category":
            cursor.execute("UPDATE products SET category = %s WHERE id = %s", (value, product_id))

        conn.commit()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def add_category(category_name):
        categories = Product.get_categories()
        if category_name in categories:
            return False

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, category) VALUES (%s, %s, %s)",
                       (f"_category_placeholder_{category_name}", 0, category_name))
        conn.commit()
        conn.close()
        return True


class Cart:
    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT quantity FROM cart WHERE user_id = %s AND product_id = %s", (user_id, product_id))
        existing = cursor.fetchone()

        if existing:
            new_quantity = existing[0] + quantity
            cursor.execute("UPDATE cart SET quantity = %s WHERE user_id = %s AND product_id = %s",
                           (new_quantity, user_id, product_id))
        else:
            cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (user_id, product_id, quantity))

        conn.commit()
        conn.close()

    @staticmethod
    def get_items(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, p.name, p.price, c.quantity, p.id
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        cart_items = cursor.fetchall()
        conn.close()
        return cart_items

    @staticmethod
    def remove_item(cart_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id = %s", (cart_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def clear(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        conn.commit()
        conn.close()


class Order:
    @staticmethod
    def create(user_id, cart_items):
        conn = get_connection()
        cursor = conn.cursor()

        total_amount = sum(item[2] * item[3] for item in cart_items)
        order_date = datetime.now()

        cursor.execute("INSERT INTO orders (user_id, total_amount, order_date) VALUES (%s, %s, %s) RETURNING id",
                       (user_id, total_amount, order_date))
        order_id = cursor.fetchone()[0]

        for item in cart_items:
            product_name, price, quantity, product_id = item[1], item[2], item[3], item[4]
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, price))

        conn.commit()
        conn.close()

        return order_id, total_amount, order_date.strftime("%Y-%m-%d %H:%M:%S")
