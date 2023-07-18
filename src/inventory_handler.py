from src.database_connector import DataBaseConnector


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

    def add_bead(self, amount):
        sql_query = f"INSERT INTO beads (shape, type, color, finishing_effect, size, amount, price) VALUES ('test', 'test_type', 'test_color', 'test_finishing_effect', 0.8, {amount}, 14.2)"
        self.connector.execute_query(sql_query)
