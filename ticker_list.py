"""Get the list of tickers from DiviData.com"""

import requests
import string
import time

from bs4 import BeautifulSoup


class GetTickers:
    """Get the tickers from DiviData.com"""
    LETTER_LIST = list(string.ascii_uppercase)

    def __init__(self):
        """Initialize the class with the given routines"""
        self.__html_data = self.__get_raw_content()
        self.__extracted_data = self.__get_content()

    def __get_raw_content(self):
        """
        Get the raw HTML data for each letter
        :return: a dictionary of raw HTML pages
        :rtype: dict
        """
        bs4_pages = list()
        for letter in self.LETTER_LIST:
            url = f"https://dividata.com/stocklist/{letter}"
            page = requests.get(url)
            print(f"Parsing url: {url}")
            bs4_pages.append(BeautifulSoup(page.text, "html.parser"))
            time.sleep(1)
        return dict(zip(self.LETTER_LIST, bs4_pages))

    def __get_content(self):
        """
        Extract the content from the downloaded raw data
        :return: a dictionary with the plain tickers
        :rtype: dict
        """

        def get_text(tag): return tag.text

        tickers_universe = dict()
        for letter in self.__html_data:
            columns = self.__html_data[letter].findAll("dl", {"class": "dl-horizontal"})
            dt_tags = [i.findAll("dt") for i in columns]
            stock_tickers = [list(map(get_text, i)) for i in dt_tags]
            stock_tickers_flatten = [ticker for sub_list in stock_tickers for ticker in sub_list]
            tickers_universe[letter] = stock_tickers_flatten
        return tickers_universe

    def get_downloaded_tickers(self):
        """
        Get the tickers
        :return: a dictionary with the downloaded data
        :rtype: dict
        """
        return self.__extracted_data
