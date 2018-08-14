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
        self.learn(self.tokeniser.title_ngrams())

    """
    Accepts a dictionary of {article_id: [list of title ngrams]} and modifies self.memory
    to learn the most likely word to follow each word in the lexicon.
    """
    def learn(self, ngrams):
        for list_of_ngrams in ngrams.values():
            for origin_word, target_word in list_of_ngrams:
                if origin_word not in self.memory:
                    self.memory[origin_word] = []
                self.memory[origin_word].append(target_word)

    """
    Return a tuple consisting of a randomly chosen next word given the current word, 
    and the probability of the next word being chosen.
    """
    def next_word(self, current_word):
        next_possible_words = self.memory.get(current_word)

        if not next_possible_words:
            next_possible_words = self.memory.keys()

    def main(self):
        pass


if __name__ == "__main__":
    markov = Markov('../data/database.db', ngram_size=2)
    markov.main()
