# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Set up a SQLite database using the given schema and create tables.
"""

import sqlite3


class Database:
    def __init__(self, path):
        self.path_to_database_file = path

    """
    Return a connection to the SQLite database.
    """

    def connect(self):
        try:
            return sqlite3.connect(self.path_to_database_file)
        except sqlite3.Error as error:
            print(error)

        return None

    def main(self):
        self.connect()


if __name__ == "__main__":
    database = Database('../data/database.db')
    database.main()
