# This software is provided under the MIT license.
# Copyright (c) 2018 Alberto Morón Hernández
# --------------------------------------------------------------------------- #
""" Populate the database with scraped data.
    Populates the following tables: 'months', 'articles'.
"""

import re
import requests
import time
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup
from utilities.Database import Database
from utilities.Helpers import Helpers as Helper


class Scraper:
    def __init__(self, homepage, database):
        self.database = Database(database)
        self.connection = self.database.connect()

        self.homepage = homepage

    """
    Scrape and create a database record for each article.
    """
    def scrape_all_articles(self):
        all_months = self.months_with_articles_to_scrape()
        article_columns = self.database.table_columns('articles')
        sql_article_where_url = " SELECT * FROM articles WHERE url = ? "

        for month in all_months:
            for article in self.scrape_articles_in_month(month):
                existing_article = Database.execute(self.connection, sql_article_where_url, (article[0],)).fetchone()

                # Skip the article if it already exists in the database.
                if existing_article:
                    existing_article = dict(zip(article_columns, existing_article))  # {column: data, ...}

                    date_published = datetime.fromtimestamp(int(existing_article['date_published'])).strftime(
                        '%Y/%m/%d')
                    print("|  An entry for {} ({}) already exists in the database.".format(
                        existing_article['title'], date_published))
                else:
                    # url, date_published, title, paragraphs = article[0], article[1], article[2], str(article[3])
                    article = dict(zip(article_columns, article))

                    sql_insert_article = " INSERT INTO articles(title, url, paragraphs, date_published) VALUES(?,?,?,?) "
                    Database.execute(self.connection,
                                     sql_insert_article,
                                     (article['title'], article['url'], article['paragraphs'], article['date_published']))
                    self.connection.commit()

                    date_published = datetime.fromtimestamp(article['date_published']).strftime('%Y/%m/%d')
                    print("+  Added article {} ({}) to the     database.".format(article['title'], date_published))

    """
    Return a list of months ['YYYY/MM', ...] for which articles have not yet been scraped.
    """
    def months_with_articles_to_scrape(self):
        months = self.update_months_table()

        if months is None or len(months) is 0:
            print("The list of months to scrape is empty. scrape_all_months() returned None.")
            return

        return ['/'.join(month) for month in months]

    """
    Populate the 'months' table with 'year, month' records.
    Return a list including the last month in the database before
    the function was called and all new months that were inserted.
    """
    def update_months_table(self):
        months = []

        sql_get_last_month = " SELECT * FROM months ORDER BY year DESC, month DESC LIMIT 1 "
        last_month = Database.execute(self.connection, sql_get_last_month, ()).fetchone()
        # If there are no entries in the 'months' table, default to 1970/01/01.
        if last_month is None:
            last_month = (0, '1970', '01')
        last_month_timestamp = Helper.to_timestamp('/'.join(last_month[1:]), '%Y/%m')

        # Scrape the homepage's sidebar for links to month subdirectories.
        page = requests.get(self.homepage).text
        for link in BeautifulSoup(page, 'html.parser').findAll('a', attrs={'href': re.compile("/\d{4}/\d{2}$")}):
            url = link.get('href')

            human_readable = url[-7:]
            link_timestamp = Helper.to_timestamp(human_readable, '%Y/%m')

            # Build a list of months not currently held in the database.
            if link_timestamp > last_month_timestamp:
                human_readable = human_readable.split('/')
                months.append((human_readable[0], human_readable[1]))

        months.reverse()  # List months in chronological order.

        if months:
            sql_insert_months = " INSERT INTO months(year, month) VALUES(?,?) "
            Database.execute_many(self.connection, sql_insert_months, months)
            self.connection.commit()
            print("\nAdded {} rows:\n{}\nto the table 'months'.\n".format(len(months), months))

        # Prepend what was previously the last entry in the 'months' table.
        if last_month[0] is not 0:
            months.insert(0, last_month[1:])

        return months

    """
    Return a list of tuples of all articles (and their metadata) for a given month.
    """
    def scrape_articles_in_month(self, month):
        urls, articles = [], []
        page = requests.get(self.homepage + month).text

        # Construct list of links and reverse it in order to get the correct chronological order.
        for link in BeautifulSoup(page, "html.parser").findAll('a', attrs={'class': 'archive'}):
            urls.append(link.get('href'))
        urls.reverse()

        for url in urls:
            articles.append(self.scrape_article(url))

        return articles

    """
    Return a payload containing article metadata and a list of the article's paragraphs.
    """
    @staticmethod
    def scrape_article(url):
        time.sleep(randint(120, 260) / 100)  # Wait between requests.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(url, headers=headers).text
        markup = BeautifulSoup(page, "html.parser")

        entry_date = markup.find('time', attrs={'class': 'entry-date'})['datetime']
        timestamp = Helper.to_timestamp(entry_date, '%Y-%m-%dT%H:%M:%S+00:00')
        title = markup.find('h1', attrs={'class': 'entry-title'}).find('a').text
        entry_content = markup.find('div', attrs={'class': 'entry-content'}).findAll('p')

        # Remove '&nbsp;', '\n'.
        paragraphs = [re.sub(u'[\xa0|\n]', u'', tag.text) for tag in entry_content]
        paragraphs = [paragraph for paragraph in paragraphs if paragraph is not '']

        payload = (url, timestamp, title, paragraphs)

        return payload

    def main(self):
        self.scrape_all_articles()


if __name__ == "__main__":
    scraper = Scraper("http://davetrott.co.uk/", '../data/database.db')
    scraper.main()
