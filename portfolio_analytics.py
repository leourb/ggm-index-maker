"""Calculate the portfolio analytics"""

from datetime import datetime, timedelta

from yahoo_data_downloader import YahooFinanceDownloader


class PortfolioAnalytics:
    """Calculate the Portfolio Analytics"""

    def __init__(self, back_test_results, back_test_years_window):
        """
        Initialize the class with the inputs
        :param pd.DataFrame back_test_results: class containing the back-test results
        :param int back_test_years_window: years to use to back-test the constructed portfolio
        """
        self.__back_test_results = back_test_results
        self.__performance = self.__calculate_performance()
        self.__start_date = str(datetime.today() - timedelta(days=(back_test_years_window * 365)))
        self.__djia_performance = self.__format_benchmark_data()
        self.__performance_vs_benchmark = self.__calculate_performance_vs_benchmark()
        self.__excess_growth_analysis = self.__analyze_excess_growth()
        self.analytics = self.__build_results()

    def __calculate_performance(self):
        """
        Calculate the performance of the portfolio
        :return: a chart with the performance
        :rtype: matplotlib.axes._subplots.AxesSubplot
        """
        return self.__back_test_results["Portfolio_Dollars"].plot(title="Portfolio Performance 1-Y Back-Test",
                                                                  grid=True,
                                                                  figsize=(10, 5)
                                                                  )

    def __format_benchmark_data(self):
        """
        Format the DataFrame to match the same format as the Portfolio data
        :return: a Pandas DataFrame with the same format as the Portfolio
        :rtype: pd.DataFrame
        """
        self.__djia_data = YahooFinanceDownloader("DJIA", self.__start_date).get_parsed_results()
        self.__djia_data = self.__djia_data[["Date", "Adj Close"]]
        self.__djia_data["Pct Change"] = self.__djia_data["Adj Close"].pct_change()
        self.__djia_data.fillna(value=0, inplace=True)
        self.__djia_data["Dollar_Performance"] = (self.__djia_data["Pct Change"] + 1).cumprod() * 100
        self.__djia_data.set_index("Date", inplace=True)
        return self.__djia_data

    def __calculate_performance_vs_benchmark(self):
        """
        Calculate the performance against the benchmark (DJIA)
        :return: a chart with the performance of the index against the benchmark
        :rtype: matplotlib.axes._subplots.AxesSubplot
        """
        self.__back_test_results["Benchmark_Performance"] = self.__djia_data["Dollar_Performance"]
        self.__back_test_results[["Portfolio_Dollars", "Benchmark_Performance"]].plot(
            title="Portfolio Performance 1-Y Back-Test vs. Benchmark", grid=True, figsize=(10, 5))

    def __analyze_excess_growth(self):
        """
        Analyze graphically the excess growth of the Portfolio over the benchmark
        :return: a histogram with the results
        :rtype: matplotlib.axes._subplots.AxesSubplot
        """
        self.__back_test_results["Excess_Return_Dollars"] = \
            self.__back_test_results["Portfolio_Dollars"] - self.__back_test_results["Benchmark_Performance"]
        return self.__back_test_results["Excess_Return_Dollars"].plot(kind="hist", grid=True)

    def __build_results(self):
        """
        Build the results returning a dictionary with all the figures
        :return: a dictionary with the figures
        :rtype: dict
        """
        results = {
            "performance": self.__performance,
            "performance_vs_benchmark": self.__performance_vs_benchmark,
            "excess_growth": self.__excess_growth_analysis
        }
        return results
