import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox


class DataBaseConnector:
    def __init__(self, database: str, database_name: str, sql_init_file: str) -> None:
        self.connection = QSqlDatabase.addDatabase(database)
        self.connection.setDatabaseName(database_name)
        self.sql_init_file = sql_init_file

    def open_connection(self) -> None:
        self.connection.open()

        if self.connection.isOpen():
            sql_select_query = QSqlQuery()
            sql_select_query.exec(
                """
                    SELECT name FROM sqlite_schema
                """
            )
            if not sql_select_query.next():
                print("Database not initiated. Creating tables.")
                self.create_database()

        else:
            QMessageBox.critical(
                None,
                "Error!",
                "Database error: %s" % self.connection.lastError().databaseText(),
            )
            sys.exit(1)

    def create_database(self) -> None:
        with open(self.sql_init_file) as sql_file:
            for line in sql_file.readlines():
                self.execute_query(line)

    @staticmethod
    def execute_query(query: str) -> QSqlQuery:
        qsql_query = QSqlQuery()
        if not qsql_query.exec(query):
            QMessageBox.critical(
                None,
                "Error!",
                f"Failed to execute query: {query}\nError: {qsql_query.lastError().databaseText()}",
            )
            sys.exit(1)
        return qsql_query
