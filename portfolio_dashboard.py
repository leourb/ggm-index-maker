"""Generate the portfolio composition, analytics and risk metrics"""

from backtest import BackTest
from component_weights import GrowthAndWeights
from risk_metrics import RiskMetrics


class PortfolioDashboard:
    """Calculate and generates the portfolio weights for each stock"""

    def __init__(self, back_test_years_window=1):
        """
        Initialize the class with the given inputs
        :param int back_test_years_window: years to use to back-test the constructed portfolio
        """
        self.__growth_and_weights = GrowthAndWeights()
        self.__backtest_results = BackTest(self.__growth_and_weights.get_ticker_list(),
                                           self.__growth_and_weights.get_component_weights(),
                                           back_test_years_window
                                           ).get_backtest_results()
        self.__risk_metrics = RiskMetrics(self.__backtest_results).results
