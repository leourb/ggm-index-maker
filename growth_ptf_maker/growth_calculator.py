"""Calculate the growth for all the US stocks"""

import os
import pickle

from ggm_calculator import InferParameters as Ip

from ticker_list import GetTickers


class CalculateG:
    """Calculate g for all the universe of US stocks"""

    def __init__(self, tickers=None):
        """
        Initialize the class with the given routines
        :param list tickers: name of the JSON file to read
        """
        self.__input_tickers = tickers
        if self.__input_tickers is None:
            self.__pickled_file_path = os.path.join(os.getcwd(), "ticker_data.pickled")
            if os.path.exists(self.__pickled_file_path):
                self.__growth_parameters = pickle.load(open(self.__pickled_file_path, "rb"))
                return
            self.__tickers = GetTickers().get_downloaded_tickers()
        else:
            self.__tickers = self.__format_ticker_list()
        self.__growth_parameters = self.__calculate_g()
        pickle.dump(self.__growth_parameters, open("ticker_data.pickled", "wb"))

    def __format_ticker_list(self):
        """
        Format the list of tickers given in input
        :return: a JSON-like data structure
        :rtype: dict
        """
        formatted_tickers = dict()
        for i in self.__input_tickers:
            key = i.upper()[0]
            if key in formatted_tickers:
                formatted_tickers[key].append(i)
                continue
            formatted_tickers[key] = list()
            formatted_tickers[key].append(i)
        return formatted_tickers

    def __calculate_g(self):
        """
        Calculate the growth parameter for all the tickers
        :return: a dictionary with the results
        :rtype: dict
        """
        growth_parameters = dict()
        for letter in self.__tickers:
            for ticker in self.__tickers[letter]:
                growth_parameters[ticker] = Ip(ticker).get_inferred_g()
                print(f"{ticker}: {growth_parameters[ticker]}")
        return growth_parameters

    def get_growth_rates(self):
        """
        Return the inferred growth rates
        :return: a dictionary with the growth rates
        :rtype: dict
        """
        return self.__growth_parameters
