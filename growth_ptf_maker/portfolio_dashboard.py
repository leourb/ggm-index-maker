"""Generate the portfolio composition, analytics and risk metrics"""

import pandas as pd

from .backtest import BackTest
from .component_weights import GrowthAndWeights
from .performance import Performance
from .portfolio_analytics import PortfolioAnalytics
from .risk_metrics import RiskMetrics


class PortfolioDashboard:
    """Calculate and generates the portfolio weights for each stock"""

    def __init__(self, back_test_years_window=1, start_date="2021-01-01", end_date=None):
        """
        Initialize the class with the given inputs
        :param int back_test_years_window: years to use to back-test the constructed portfolio
        """
        self.__growth_and_weights = GrowthAndWeights()
        self.__weights = pd.read_csv("weights.csv", index_col=0)
        self.__back_test_results = BackTest(self.__growth_and_weights.get_ticker_list(),
                                            self.__weights,
                                            back_test_years_window
                                            )
        self.__risk_metrics = RiskMetrics(self.__back_test_results).results
        self.__portfolio_analytics = PortfolioAnalytics(self.__growth_and_weights.get_growth_rates(),
                                                        self.__back_test_results, back_test_years_window).results
        self.__portfolio_returns = Performance(start_date, end_date).portfolio_returns()

    def back_test_results(self):
        """
        Return the back-test results
        :return: the results of the back-test
        :rtype: dict
        """
        results = {
            "weights": self.__back_test_results.get_weights(),
            "back_test": self.__back_test_results.get_back_test_results()
        }
        return results

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

    def portfolio_returns(self):
        """
        Return the portfolio returns
        :return: the returns calculated from the given range
        :rtype: pd.DataFrame
        """
        return self.__portfolio_returns

    def update_weights(self):
        """
        Replace the weights CSV file with the current calculated weights
        :return: a saved CSV file
        :rtype: csv
        """
        return self.__growth_and_weights.update_weights()
