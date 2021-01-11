"""Module to get the list of tickers from Wikipedia"""

import requests

from bs4 import BeautifulSoup


class GetTickers:
    """Get tickers from Wikipedia"""

    def __init__(self):
        """Executes the functions when the class is created"""
        self.__tickers = self.__parse_tickers()

    def __parse_tickers(self):
        """
        Get the tickers from Wikipedia
        :return: a list of tickers
        :rtype: list
        """
        wiki_page = requests.get("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average").text
        parsed_page = BeautifulSoup(wiki_page, "html.parser")
        tickers_table = parsed_page.find(id="constituents")
        a_tags = [row.findAll("a") for row in tickers_table.findAll("td") if row.findAll("a")]
        flatten_tags = list()
        for element in a_tags:
            if len(element) > 1:
                for tag in element:
                    flatten_tags.append(tag)
            else:
                flatten_tags.append(element[0])
        tickers = list()
        for element in flatten_tags:
            if element.get("rel"):
                tickers.append(element.get_text())
        return tickers

    def get_tickers(self):
        """
        Return the list of tickers
        :return: a list with the tickers
        :rtype: list
        """
        return self.__tickers
