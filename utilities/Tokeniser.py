# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Tokenise the corpus and generate ngrams.
"""

from utilities.Database import Database


class Tokeniser:
    def __init__(self, database, ngram_size):
        self.database = Database(database)
        self.connection = self.database.connect()

        self.ngram_size = ngram_size

    def main(self):
        pass


if __name__ == "__main__":
    tokeniser = Tokeniser('../data/database.db', 2)
    tokeniser.main()
