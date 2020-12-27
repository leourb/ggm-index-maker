"""Generate the portfolio composition, analytics and risk metrics"""

import pandas as pd

from backtest import BackTest
from component_weights import GrowthAndWeights
from portfolio_analytics import PortfolioAnalytics
from risk_metrics import RiskMetrics


class PortfolioDashboard:
    """Calculate and generates the portfolio weights for each stock"""

    def __init__(self, back_test_years_window=1):
        """
        Initialize the class with the given inputs
        :param int back_test_years_window: years to use to back-test the constructed portfolio
        """
        self.__growth_and_weights = GrowthAndWeights()
        self.__back_test_results = BackTest(self.__growth_and_weights.get_ticker_list(),
                                            self.__growth_and_weights.get_component_weights(),
                                            back_test_years_window
                                            )
        self.__risk_metrics = RiskMetrics(self.__back_test_results).results
        self.__portfolio_analytics = PortfolioAnalytics(self.__growth_and_weights.get_growth_rates(),
                                                        self.__back_test_results, back_test_years_window)

    def back_test_results(self):
        """
        Return the back-test results
        :return: the results of the back-test ran
        :rtype: pd.DataFrame
        """
        return self.__back_test_results.get_back_test_results()

    def risk_metrics(self):
        """
        Return the risk metrics results
        :return: the results of the calculated risk metrics
        :rtype: dict
        """
        return self.__risk_metrics

    def analytics(self):
        """
        Return the analytics of the Portfolio
        :return: the portfolio analytics object
        :rtype: dict
        """
        return self.__portfolio_analytics
