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

    """
    Create a table from a given SQL statement.
    """
    def create_table(self, connection, create_table_sql):
        try:
            self.execute(connection, create_table_sql, ())
        except sqlite3.Error as error:
            print(error)

    """
    Return a list of SQL statements used by build_schema to generate tables.
    """
    @staticmethod
    def table_creation_sql_statements():
        statements = [
            """ CREATE TABLE IF NOT EXISTS months (
                   id             integer PRIMARY KEY,
                   year           text    NOT NULL,
                   month          text    NOT NULL
                 );""",
            """ CREATE TABLE IF NOT EXISTS articles (
                   id             integer PRIMARY KEY,
                   title          text    NOT NULL,
                   url            text    NOT NULL,
                   paragraphs     text    NOT NULL,
                   date_published integer NOT NULL
                 );""",
        ]

        return statements

    """
    Execute a single SQL statement.
    """
    @staticmethod
    def execute(connection, sql_statement, data):
        try:
            return connection.cursor().execute(sql_statement, data)
        except sqlite3.Error as error:
            print(error)

    """
    Execute multiple SQL statements.
    """
    @staticmethod
    def execute_many(connection, sql_statement, data):
        try:
            return connection.cursor().executemany(sql_statement, data)
        except sqlite3.Error as error:
            print(error)

    def main(self):
        self.build_schema()


if __name__ == "__main__":
    database = Database('../data/database.db')
    database.main()
