from PyQt6.QtSql import QSqlQuery

from src.entities.inventory import Inventory
from src.database.dao.component_dao import ComponentDAO


class InventoryDAO:
    def __init__(self):
        pass

    def update(self, inventory_id: int, inventory: Inventory):
        query = QSqlQuery()
        query.prepare(f"UPDATE inventory SET component_id = :component_id, amount = :amount,"
                      "other = :other, unit_price = :unit_price, total_price = :total_price, add_date = :add_date "
                      "WHERE inventory_id = :inventory_id")

        query.bindValue(":component_id", inventory.component_id)
        query.bindValue(":amount", inventory.amount)
        query.bindValue(":other", inventory.other)
        query.bindValue(":unit_price", inventory.unit_price)
        query.bindValue(":total_price", inventory.total_price)
        query.bindValue(":add_date", inventory.add_date)
        query.bindValue(":inventory_id", inventory_id)

        result = query.exec()
        return result, query.lastError().text()

    def insert(self, inventory: Inventory) -> (bool, str):
        if inventory.component_id == -1:
            component_dao = ComponentDAO()

            inventory.component_id = component_dao.get_component_id_or_insert(inventory.component)

        query = QSqlQuery()
        query.prepare("INSERT INTO inventory(component_id, amount, other, unit_price, total_price, add_date)"
                      "VALUES(:component_id, :amount, :other, :unit_price, :total_price, :add_date)")

        query.bindValue(":component_id", inventory.component_id)
        query.bindValue(":amount", inventory.amount)
        query.bindValue(":other", inventory.other)
        query.bindValue(":unit_price", inventory.unit_price)
        query.bindValue(":total_price", inventory.total_price)
        query.bindValue(":add_date", inventory.add_date)

        result = query.exec()
        return result, query.lastError().text()

    def delete(self, inventory_id: int):
        query = QSqlQuery()
        query.prepare(f"DELETE FROM inventory WHERE inventory_id={inventory_id}")

        result = query.exec()
        return result, query.lastError().text()

    def get_total_spend(self):
        query = QSqlQuery()
        query.prepare("SELECT SUM(total_price) FROM inventory")

        result = query.exec()
        if result:
            query.next()
            return query.value(0), ""
        else:
            return result, query.lastError().text()
