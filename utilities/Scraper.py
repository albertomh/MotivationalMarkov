# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Populate the database with scraped data.
"""

from utilities.Database import Database


class Scraper:
    def __init__(self, homepage, database):
        self.homepage = homepage
        self.database = Database(database)

        self.connection = self.database.connect()

    def main(self):
        return


if __name__ == "__main__":
    scraper = Scraper("http://davetrott.co.uk/", '../data/database.db')
    scraper.main()
