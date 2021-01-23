"""Module to compute the performance of the portfolio"""

from functools import reduce

import pandas as pd

from .yahoo_data_downloader import YahooFinanceDownloader


class Performance:
    """Calculate the performance of the portfolio from a given date given weights saved in dir"""

    def __init__(self, start_date, end_date):
        """
        Initialize the class with the given inputs
        :param str start_date: start date of the performance
        :param str end_date: end date of the performance
        """
        self.__weights = pd.read_csv("weights.csv", index_col=0)
        self.__historical_data = [{i: YahooFinanceDownloader(i, start_date, end_date)}
                                  for i in self.__weights.index.tolist()]
        self.__formatted_data = self.__format_and_reshape_historical_data()
        self.__returns = self.__calculate_portfolio_returns()

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
                    series_df = series[ticker].get_parsed_results()
                    temp_df = series_df[["Date", "Adj Close"]]
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

    def portfolio_returns(self):
        """
        Return the portfolio returns
        :return: a pd.DataFrame with the portfolio returns
        :rtype: pd.DataFrame
        """
        return self.__returns
