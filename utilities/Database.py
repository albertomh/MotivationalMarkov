# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Set up a SQLite database using the given schema and create tables.
"""


class Database:
    def __init__(self, path):
        self.path_to_database_file = path

    def main(self):
        return


if __name__ == "__main__":
    database = Database('../data/database.db')
    database.main()
