"""Download historical data and Back-Test the created portfolio"""

from datetime import datetime, timedelta
from functools import reduce

import pandas as pd

from .yahoo_data_downloader import YahooFinanceDownloader


class BackTest:
    """Back-Test the created portfolio"""

    def __init__(self, tickers, weights, years=1):
        """
        Initialize the class
        :param list tickers: list of tickers to get historical data from
        :param pd.DataFrame weights: DataFrame with the weights of the components
        :param int years: years to back-test
        """
        self.__years = int(years)
        self.__weights = weights
        self.__historical_data = self.__download_historical_data(tickers, self.__years)
        self.__formatted_data = self.__format_and_reshape_historical_data()
        self.__portfolio_historical_returns = self.__calculate_portfolio_returns()

    def __download_historical_data(self, tickers, years=1):
        """
        Back-test the created portfolio to evaluate the performance of the Zero-Investment Portfolio
        :param list tickers: list of tickers to get historical data from
        :param int years: years to back-test
        :return: a list of object with Pandas DataFrame of historical data for each ticker
        :rtype: list
        """
        start_date = str(datetime.today() - timedelta(days=(years * 365)))
        historical_data = [{i: YahooFinanceDownloader(i, start_date).get_parsed_results()} for i in tickers]
        return historical_data

    def __format_and_reshape_historical_data(self):
        """
        Format and reshape the downloaded historical data
        :return: a Pandas DataFrame with the data
        :rtype: pd.DataFrame
        """
        formatted_data = list()
        for series in self.__historical_data:
            for ticker in series:
                if ticker in self.__weights.index.tolist():
                    temp_df = series[ticker][["Date", "Adj Close"]]
                    temp_df.columns = ["Date", ticker]
                    formatted_data.append(temp_df)
        merged_series = reduce(lambda x, y: pd.merge(x, y, on="Date"), formatted_data)
        merged_series.set_index("Date", inplace=True)
        return merged_series

    def __calculate_portfolio_returns(self):
        """
        Calculate portfolio returns given a DataFrame with Historical Prices
        :return: a DataFrame with the portfolio returns
        :rtype: pd.DataFrame
        """
        components_return = self.__formatted_data.pct_change()
        for ticker in components_return.columns:
            components_return[ticker] = (components_return[ticker] * self.__weights["weights"][ticker]) + 1
        components_return["Portfolio"] = components_return.product(axis=1)
        components_return["Portfolio_Dollars"] = components_return["Portfolio"].cumprod() * 100
        return components_return

    def get_back_test_results(self):
        """
        Get the calculated back-tested results
        :return: a Pandas DataFrame with the calculated results
        :rtype: pd.DataFrame
        """
        return self.__portfolio_historical_returns

    def get_weights(self):
        """
        Return the calculated weights
        :return: the vector with the weights
        :rtype: pd.DataFrame
        """
        return self.__weights
