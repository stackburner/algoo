from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import quandl
import configparser
import os
import os.path


class Reader:

    def __init__(self):
        """
        Reader class that reads data from both quandl and alpha vantage
        """
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        quandl.ApiConfig.api_key = self.config['QUANDL']['key']
        self.ts = TimeSeries(key=self.config['ALPHAVANTAGE']['key'], output_format='pandas')

    def q_get(self, data, ticker):
        """
        Quandl get method that is dynamic to the extend that all datasets
        as defined in the config file can be fetched
        Data is loaded only once from the remote host and then saved in a
        local csv under .../data/ to prevent api overloading
        :param data: Dataset as defined in the config
        :param ticker: Ticker as defined on quandl
        :return: pandas dataframe,  path to the csv
        Usage: Reader().q_get('index_data', 'NQGI'))
        """
        file_path = '{0}/data/{1}{2}.csv'.format(os.getcwd(), data, ticker)
        if not os.path.exists(file_path):
            df = quandl.get('{0}{1}'.format(self.config['QUANDL'][data], ticker))
            df.to_csv(file_path)

            return df, file_path
        else:

            return pd.read_csv(file_path), file_path

    def a_get_daily(self, ticker):
        """
        Alpha vantage get method for adjusted daily EOD time series.
        Data is loaded only once from the remote host and then saved in a
        local csv under .../data/ to prevent api overloading
        :param ticker: Ticker as defined on alpha vantage
        :return: pandas dataframe, path to the csv
        Usage: Reader().a_get_daily('IWLE.DE')
        """
        file_path = '{0}/data/{1}.csv'.format(os.getcwd(), ticker)
        if not os.path.exists(file_path):
            df, meta = self.ts.get_daily_adjusted(symbol=ticker, outputsize='full')
            df.sort_index(inplace=True)
            df.to_csv(file_path)

            return df, file_path
        else:

            return pd.read_csv(file_path), file_path
