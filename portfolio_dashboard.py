"""Generate the portfolio taking as input the inferred growth rates"""

import pickle

import pandas as pd

from scipy.stats import norm

from backtest import BackTest
from datashelf import DataShelf
from growth_calculator import CalculateG
from risk_metrics import RiskMetrics


class PortfolioDashboard:
    """Calculate and generates the portfolio weights for each stock"""

    def __init__(self, back_test_years_window=1):
        """
        Initialize the class with the given inputs
        :param int back_test_years_window: years to use to back-test the constructed portfolio
        """
        self.__ticker_list = DataShelf().get_ticker_list()
        self.__growth_rates = CalculateG(self.__ticker_list).get_growth_rates()
        self.__growth_rates = pickle.load(open("growth_rates.pickled", "rb"))
        self.__component_weights = self.__calculate_component_weight()
        self.__backtest_results = BackTest(self.__ticker_list,
                                           self.__component_weights,
                                           back_test_years_window
                                           ).get_backtest_results()
        self.__risk_metrics = RiskMetrics(self.__backtest_results).results

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
