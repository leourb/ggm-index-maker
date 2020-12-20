"""Calculate the growth for all the US stocks"""

from ggm_calculator import InferParameters as IP

from ticker_list import GetTickers


class CalculateG:
    """Calculate g for all the universe of US stocks"""

    def __init__(self):
        """Initialize the class with the given routines"""
        self.__tickers = GetTickers().get_downloaded_tickers()
        self.__growth_parameters = self.__calculate_g()

    def __calculate_g(self):
        """
        Calculate the growth parameter for all the tickers
        :return: a dictionary with the results
        :rtype: dict
        """
        growth_parameters = dict()
        for letter in self.__tickers:
            for ticker in self.__tickers[letter]:
                growth_parameters[ticker] = IP(ticker).get_inferred_g()
                print(growth_parameters)
        return growth_parameters
