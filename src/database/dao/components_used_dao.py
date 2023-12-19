from PyQt6.QtSql import QSqlQuery

from src.entities.product import ComponentsUsed


class ComponentsUsedDAO:
    def __init__(self):
        pass

    @staticmethod
    def get_components_used_by_product_id(product_name: str):
        query = QSqlQuery()
        query.prepare(
            f"SELECT * FROM components_used WHERE product_name == "
            f"\"{product_name}\"")

        result = query.exec()
        if result:
            components_used = []
            while query.next():
                components_used.append(ComponentsUsed(query.value(0), query.value(1), query.value(3), query.value(4),
                                                      query.value(5)))
            return components_used, ""
        else:
            return result, query.lastError().text()

    @staticmethod
    def get_components_used_by_project_id(project_name: str):
        query = QSqlQuery()
        query.prepare(
            f"SELECT * FROM components_used WHERE project_name == "
            f"\"{project_name}\"")

        result = query.exec()

        if result:
            components_used = []
            while query.next():
                components_used.append(ComponentsUsed(query.value(0), query.value(1), query.value(3), query.value(4),
                                                      query.value(5)))
            return components_used, ""
        else:
            return result, query.lastError().text()
