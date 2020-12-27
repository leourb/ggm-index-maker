"""Stores static data"""

MY_LIST = ['AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW', 'GS', 'HD', 'HON', 'IBM',
                     'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ',
                     'WBA', 'WMT']


class DataShelf:
    """Static data container"""

    def __init__(self):
        """Initialize the class with the static data"""
        self.__ticker_list = MY_LIST

    def get_ticker_list(self):
        """
        Return the saved ticker list
        :return: the saved ticker list
        :rtype: list
        """
        return self.__ticker_list
