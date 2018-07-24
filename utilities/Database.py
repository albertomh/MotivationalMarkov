# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Set up SQLite database using the given schema and create tables.
    Provide access to the database through the connect() method.
"""

import sqlite3
from pathlib import Path


class Database:
    def __init__(self, path):
        self.path_to_database_file = path

        if not Path(path).is_file():
            self.build_schema()

    """
    Return a connection to the SQLite database.
    """
    def connect(self):
        try:
            return sqlite3.connect(self.path_to_database_file)
        except sqlite3.Error as error:
            print(error)

        return None

    """
    Build the database schema and create each table in table_creation_sql_statements.
    """
    def build_schema(self):
        connection = self.connect()
        if connection is not None:
            for statement in self.table_creation_sql_statements():
                self.create_table(connection, statement)
        else:
            print("Error: cannot create the database connection.")

    def main(self):
        self.build_schema()


if __name__ == "__main__":
    database = Database('../data/database.db')
    database.main()
