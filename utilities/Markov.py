# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Generate utterances using Markov chains.
"""

from utilities.Database import Database
from utilities.Tokeniser import Tokeniser


class Markov:
    def __init__(self, database, ngram_size):
        self.database = Database(database)
        self.connection = self.database.connect()

        self.tokeniser = Tokeniser(database, ngram_size)
        self.original_titles = self.tokeniser.all_article_titles()

        self.memory = {}

    """
    """
    def learn(self, ngrams):
        pass

    def main(self):
        pass


if __name__ == "__main__":
    markov = Markov('../data/database.db', ngram_size=2)
    markov.main()
