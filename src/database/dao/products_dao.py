from PyQt6.QtSql import QSqlQuery

from src.entities.product import Product
from src.database.dao.component_dao import ComponentDAO


class ProductsDAO:
    def __init__(self):
        pass

    def get_product_by_name(self, product_name: str):
        query = QSqlQuery()
        query.prepare(
            f"SELECT * FROM products WHERE product_name == "
            f"\"{product_name}\"")

        result = query.exec()
        if result:
            product = []
            while query.next():
                i = 0
                while query.value(i):
                    product.append(query.value(i))
                    i += 1
            if product:
                return Product(*product), ""
            else:
                return [], "No product in DB"
        else:
            return result, query.lastError().text()

    def get_product_names(self):
        query = QSqlQuery()
        query.prepare(f"SELECT product_name from products")

        result = query.exec()
        if result:
            products = []
            while query.next():
                products.append(query.value(0))
            return products, ""
        else:
            return result, query.lastError().text()
