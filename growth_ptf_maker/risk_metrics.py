"""Calculate Risk Metrics for the simulated Portfolio"""

import numpy as np

from scipy.stats import norm

from .backtest import BackTest

class RiskMetrics:
    """Calculate the risk indicators for the portfolio"""

    def __init__(self, back_test_data):
        """
        Initialize the class with the given parameters
        :param BackTest back_test_data: Pandas DataFrame with the back-tested data
        """
        self.__back_tested_data = back_test_data.get_back_test_results()
        self.__var_95 = self.__calculate_var(95)
        self.__var_99 = self.__calculate_var(99)
        self.__es_97_5 = self.__calculate_es(97.5)
        self.__hvar_95 = self.__calculate_hvar(95)
        self.__hvar_99 = self.__calculate_hvar(99)
        self.__min = self.__back_tested_data["Portfolio"].min() - 1
        self.__min_max_range = (self.__back_tested_data["Portfolio"].max() -
                                self.__back_tested_data["Portfolio"].min()) - 1
        self.results = self.__build_results()

    def __calculate_var(self, confidence):
        """
        Calculate the Market Risk using the Parametric VaR approach given a confidence level
        :param float confidence: VaR confidence level
        :return: the calculated VaR value
        :rtype: float
        """
        z = norm.ppf(confidence/100)
        std = self.__back_tested_data["Portfolio"].std()
        var = std * z
        return var

    def __calculate_es(self, confidence):
        """
        Calculate the Expected Shortfall with the given confidence interval
        :param float confidence: ES confidence level
        :return: the calculated ES value
        :rtype: float
        """
        mu = self.__back_tested_data["Portfolio"].mean() - 1
        sigma = self.__back_tested_data["Portfolio"].std()
        x = confidence / 100
        u = norm.ppf(x)
        es = mu + sigma * (np.exp(-u**2/2)/((1-x) * np.sqrt(2*np.pi)))
        return es

    def __calculate_hvar(self, confidence):
        """
        Calculate the Historical VaR for the given pd.Series
        :param float confidence: HVaR confidence level
        :return: the calculated HVaR value
        :rtype: float
        """
        series = self.__back_tested_data["Portfolio"] - 1
        series.sort_values(ascending=False, inplace=True)
        index_val = round(confidence / 100 * len(series))
        return np.abs(series.iloc[index_val])

    def __build_results(self):
        """
        Build the results in a dictionary to be stored
        :return: a dictionary with all the calculated results
        :rtype: dict
        """
        results = {
            "var95": self.__var_95,
            "var99": self.__var_99,
            "hvar95": self.__hvar_95,
            "hvar99": self.__hvar_99,
            "es975": self.__es_97_5,
            "min": self.__min,
            "min_max_range": self.__min_max_range
        }
        return results
