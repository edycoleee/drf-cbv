#product/services.py
from myproject.utils.db import get_cursor_dict


class ProductService:
    @staticmethod
    def get_all_products():
        with get_cursor_dict() as cursor:
            cursor.execute("SELECT * FROM tb_products")
            return cursor.fetchall()

    @staticmethod
    def get_product_by_id(product_id):
        with get_cursor_dict() as cursor:
            cursor.execute("SELECT * FROM tb_products WHERE id = %s", [product_id])
            return cursor.fetchone()

    @staticmethod
    def create_product(prod_name, price):
        with get_cursor_dict() as cursor:
            cursor.execute("INSERT INTO tb_products (prod_name, price) VALUES (%s, %s)", [prod_name, price])
            new_id = cursor.lastrowid
            return {"id": new_id, "prod_name": prod_name, "price": price}

    @staticmethod
    def update_product(product_id, prod_name, price):
        with get_cursor_dict() as cursor:
            cursor.execute("UPDATE tb_products SET prod_name = %s, price = %s WHERE id = %s", [prod_name, price, product_id])
            if cursor.rowcount == 0:
                return None
            return {"id": int(product_id), "prod_name": prod_name, "price": price}

    @staticmethod
    def delete_product(product_id):
        with get_cursor_dict() as cursor:
            cursor.execute("DELETE FROM tb_products WHERE id = %s", [product_id])
            return cursor.rowcount > 0