import sys

from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox


class DataBaseConnector:
    def __init__(self):
        self.connection = QSqlDatabase.addDatabase('QSQLITE')
        self.connection.setDatabaseName('sql/inventory.sqlite')

    def open_connection(self):
        self.connection.open()

        if self.connection.isOpen():
            sql_select_query = QSqlQuery()
            sql_select_query.exec(
                """
                    SELECT name FROM sqlite_schema
                """
            )
            if not sql_select_query.next():
                print("Brak schemy bazy danych. Tworze tabele.")
                self.create_database()

        else:
            QMessageBox.critical(
                None,
                "Error!",
                "Błąd bazy danych: %s" % self.connection.lastError().databaseText(),
                )
            sys.exit(1)

    def create_database(self):
        create_tables_query = QSqlQuery()
        with open('sql/db_tables_create.sql') as sql_file:
            for line in sql_file.readlines():
                create_tables_query.exec(line)