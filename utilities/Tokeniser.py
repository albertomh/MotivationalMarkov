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

    """
    Return a list of ngrams of size 'self.ngram_size' for the given list of tokens.
    """
    @staticmethod
    def ngram(tokens, ngram_size):
        number_of_tokens = len(tokens)
        ngrams = []

        # Halt program execution for invalid values of n.
        if ngram_size == 0 or ngram_size > (number_of_tokens - 2):  # Subtract 2 to account for the insertion of utterance start/end tokens.
            raise ValueError("The value of ngram_size cannot be 0 or larger than the number of tokens in the shortest utterance.")

        for token_number in range(number_of_tokens):
            first_ngram = last_ngram = list()

            if token_number == 0:
                # Handle first ngram.
                for token in range(0, ngram_size):
                    first_ngram.append(tokens[token])
                ngrams.append(tuple(first_ngram))

            elif token_number == number_of_tokens-1:
                # Handle last ngram.
                for token in range(number_of_tokens - ngram_size, number_of_tokens):
                    last_ngram.append(tokens[token])
                ngrams.append(tuple(last_ngram))

        return ngrams

    """
    Return a dictionary of the form {article_id: ['_^', 'word1', ..., 'word_n','$_'], ...}
    """
    def tokenise_titles(self, article_titles=None):
        if article_titles is None:
            article_titles = self.all_article_titles()

        tokenised_titles = dict((id_number, title.split(' ')) for (id_number, title) in article_titles)

        for title in tokenised_titles.values():
            title.insert(0, '_^')  # Utterance start marker.
            title.append('$_')     # Utterance end marker.

        return tokenised_titles

    """
    Return a list of all the titles in the 'articles' table of the form [(id, 'title'), ...].
    """
    def all_article_titles(self):
        sql_all_article_titles = " SELECT id, title FROM articles WHERE title IS NOT NULL "
        all_article_titles = Database.execute(self.connection, sql_all_article_titles, ()).fetchall()

        # Add a space before punctuation so that it can be tokenised.
        all_article_titles = [(title[0], title[1].replace('?', ' ?')) for title in all_article_titles]

        return all_article_titles

    def main(self):
        self.all_article_titles()


if __name__ == "__main__":
    tokeniser = Tokeniser('../data/database.db', 2)
    tokeniser.main()
