# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Scrape articles and store them in the database. """


class Scraper(object):
    def __init__(self, homepage):
        self.homepage = homepage

    def main(self):
        return


if __name__ == "__main__":
    scraper = Scraper("http://davetrott.co.uk/")
    scraper.main()
