"""Calculate the growth for all the US stocks"""

import pickle

from ggm_calculator import InferParameters as Ip

from ticker_list import GetTickers


class CalculateG:
    """Calculate g for all the universe of US stocks"""

    def __init__(self):
        """Initialize the class with the given routines"""
        self.__tickers = GetTickers().get_downloaded_tickers()
        self.__growth_parameters = self.__calculate_g()
        pickle.dump(self.__growth_parameters, open("ticker_data.pickled", "wb"))

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
                print(growth_parameters[ticker])
        return growth_parameters

    def get_growth_rates(self):
        """
        Return the inferred growth rates
        :return: a dictionary with the growth rates
        :rtype: dict
        """
        return self.__growth_parameters
