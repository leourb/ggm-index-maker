"""Component Weights and Growth calculator"""

import os

import pandas as pd

from scipy.stats import norm

from .datashelf import DataShelf
from .growth_calculator import CalculateG


class GrowthAndWeights:
    """Class to calculate the growth and weights for the stocks in input"""

    def __init__(self):
        """Initialize the class with the given inputs"""
        self.__ticker_list = DataShelf().get_ticker_list()
        self.__growth_rates = CalculateG(self.__ticker_list).get_growth_rates()
        self.__component_weights = self.__calculate_component_weight()
        if not os.path.isfile("weights.csv"):
            self.__component_weights.to_csv("weights.csv")

    def __calculate_component_weight(self):
        """
        Calculate the component weights to construct a Zero-Investment Portfolio
        :return: a Pandas DataFrame with the calculated weights
        :rtype: pd.DataFrame
        """
        growth_df = pd.DataFrame(index=list(self.__growth_rates.keys()), data={"g": list(self.__growth_rates.values())})
        growth_df.dropna(inplace=True)
        growth_df["z-score"] = (growth_df["g"] - growth_df["g"].mean()) / growth_df["g"].std()
        growth_df["cdf"] = norm.cdf(growth_df["z-score"])
        growth_df["weights"] = growth_df["cdf"] - 0.5
        return growth_df

    def get_ticker_list(self):
        """
        Get ticker list as a public member
        :return: a list of tickers
        :rtype: list
        """
        return self.__ticker_list

    def get_growth_rates(self):
        """
        Get the inferred growth rates
        :return: a dictionary with the growth rates
        :rtype: dict
        """
        return self.__growth_rates

    def get_component_weights(self):
        """
        Get the component weights as a public member
        :return: a Pandas DataFrame with the weights
        :rtype: pd.DataFrame
        """
        return self.__component_weights

    def update_weights(self):
        """
        Replace the weights CSV file with the current calculated weights
        :return: a saved CSV file
        :rtype: csv
        """
        return self.__component_weights.to_csv("weights.csv")
