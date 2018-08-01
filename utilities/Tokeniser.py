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
    Return a list of all the titles in the 'articles' table of the form [(article_id, 'title'), ...].
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
