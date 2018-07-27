# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Populate the database with scraped data.
    Populates the following tables: 'months', 'articles'.
"""

from utilities.Database import Database
from utilities.Helpers import Helpers as Helper


class Scraper:
    def __init__(self, homepage, database):
        self.homepage = homepage
        self.database = Database(database)

        self.connection = self.database.connect()

    """
    """
    def update_months_table(self):
        months = []

        sql_get_last_month = " SELECT * FROM months ORDER BY year DESC, month DESC LIMIT 1 "
        last_month = Database.execute(self.connection, sql_get_last_month, ()).fetchone()
        # If there are no entries in the 'months' table, default to 1970/01/01.
        if last_month is None:
            last_month = (0, '1970', '01')
        last_month_timestamp = Helper.to_timestamp('/'.join(last_month[1:]), '%Y/%m')

        return months

    def main(self):
        self.update_months_table()


if __name__ == "__main__":
    scraper = Scraper("http://davetrott.co.uk/", '../data/database.db')
    scraper.main()
