from src.database_connector import DataBaseConnector
from PyQt6.QtSql import QSqlQuery


class InventoryHandlerMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class InventoryHandler(metaclass=InventoryHandlerMeta):
    def __init__(self, database_connector: DataBaseConnector):
        self.connector = database_connector(
            database_name="sql/inventory.sqlite",
            sql_init_file="sql/db_tables_create.sql",
        )
        self.connector.open_connection()

    def populate_with_test_data(self):
        for i in range(100):
            self.connector.execute_query(
                f'INSERT INTO items'
                f'(material, type, shape, color, finishing_effect, size, amount, other, unit_price, total_price)'
                f'VALUES ("{"test_matherial_" + str(i)}", "{"test_type_" + str(i)}", "{"test_shape_" + str(i)}",'
                f'"{"test_color_" + str(i)}", "{"test_size_" + str(i)}", {i}, {i}, {i}, {i}, {i})'
            )
