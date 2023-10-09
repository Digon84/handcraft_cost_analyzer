from src.database.database_connector import DataBaseConnector


class SqliteConnector(DataBaseConnector):
    def __init__(self, database_name, sql_init_file):
        super().__init__("QSQLITE", database_name, sql_init_file)
