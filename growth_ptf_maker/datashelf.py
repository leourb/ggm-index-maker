"""Stores static data"""

from .refresh_tickers import GetTickers


class DataShelf:
    """Static data container"""

    def __init__(self):
        """Initialize the class with the static data"""
        self.__ticker_list = sorted(GetTickers().get_tickers())

    def get_ticker_list(self):
        """
        Return the saved ticker list
        :return: the saved ticker list
        :rtype: list
        """
        return self.__ticker_list
