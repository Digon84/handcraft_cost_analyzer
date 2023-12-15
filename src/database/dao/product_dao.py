from PyQt6.QtSql import QSqlQuery

from src.entities.inventory import Inventory
from src.database.dao.component_dao import ComponentDAO


class ProductDAO:
    def __init__(self):
        pass

    def get_product_names(self):
        query = QSqlQuery()
        query.prepare(f"SELECT product_name from product")

        result = query.exec()
        if result:
            products = []
            while query.next():
                products.append(query.value(0))
            return products, ""
        else:
            return result, query.lastError().text()
