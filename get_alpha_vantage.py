# This script gets data from the AlphaVantage api.
# This script contains functions that access and analyse ETF holdings
# data. This is useful for portfolio construction and and analysis.


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
#from urllib import urlretrieve
import requests
import datetime
import pickle
#import xlrd

import utensils.json_manip as jm


def get_fundamental_income(ticker):
    """
    Get the Income Statement information going back 5 years for the given ticker.
    This communicates with the Alpha Vantage API, so you need an internet connection.
    It returns the JSON version. Because API calls are limited, we isolate this 
    function, then save with pickle, and format with format_fundamental_income().
    """
    #
    base = r"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol="
    end = "&apikey=5ELABCNC7WUW0H21"
    url = base + ticker.upper() + end
    #print(url)
    resp = requests.get(url)
    data = resp.json()

    return data


def get_fundamental_balance(ticker):
    """
    Get the Balance Sheet Statement information going back 5 years for the
    given ticker. This communicates with the Alpha Vantage API, so you need
    an internet connection. It returns the JSON version. Because API calls 
    are limited, we isolate this function, then save with pickle, and format
    with format_fundamental_income().
    """
    #
    base = r"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="
    end = "&apikey=5ELABCNC7WUW0H21"
    url = base + ticker.upper() + end
    #print(url)
    resp = requests.get(url)
    data = resp.json()

    return data


def get_fundamental_cashflow(ticker):
    """
    Get the Cash Flow Statement information going back 5 years for the
    given ticker. This communicates with the Alpha Vantage API, so you need
    an internet connection. It returns the JSON version. Because API calls 
    are limited, we isolate this function, then save with pickle, and format
    with format_fundamental_income().
    """
    #
    base = r"https://www.alphavantage.co/query?function=CASH_FLOW&symbol="
    end = "&apikey=5ELABCNC7WUW0H21"
    url = base + ticker.upper() + end
    #print(url)
    resp = requests.get(url)
    data = resp.json()

    return data





def read_tickers(file_name):
    """
    Reads in the file with tickers saved as a comma-separated list and returns
    them as a Python list.
    """

    my_file = open("sp500_tickers.txt", 'r')
    tickers = my_file.read()
    tckrs_list = tickers.replace(' ', '').replace('\n', '').split(',')

    my_file.close()

    return tckrs_list

class OneStock:
    """
    This class holds information pertaining to one stock ticker. This can be
    everything from fundamental data to technical info.
    """
    def __init__(self, ticker):

        self.ticker = ticker

    def get_fundamental(self, get_income, get_balance, get_cashflow):

        if get_income:
            self.income = get_fundamental_income(self.ticker)

        if get_balance:
            self.balance = get_fundamental_balance(self.ticker)

        if get_balance:
            self.cashflow = get_fundamental_cashflow(self.ticker)

    def convert_fund_to_df(self, do_income, do_balance, do_cashflow):

        if do_income:
            self.income_df = jm.fundamental_to_df(self.income)

        if do_balance:
            self.balance_df = jm.fundamental_to_df(self.balance)

        if do_cashflow:
            self.cashflow_df = jm.fundamental_to_df(self.cashflow)


class StockBasket:
    """
    This class holds information for a bunch of stocks, such as an ETF or portfolio
    or just a random assortment that I want information/modeling on.
    """
    def __init__(self, ticker_list):

        self.tickers = ticker_list
        self.stocks = []
        for tckr in self.tickers:
            self.stocks.append(OneStock(tckr))
            

    def get_fundamentals(self, get_income, get_balance, get_cashflow):
        """
        Get fundamental information for all the stocks specified in the 
        ticker list. To save API calls, only get the information you're
        missing with get_ boolean variables.
        """

        for stock in self.stocks:
            stock.get_fundamental(get_income, get_balance, get_cashflow)


    def convert_fund_to_df(self, do_income, do_balance, do_cashflow):
        """
        Convert the JSON files downloaded from the API into Pandas DataFrames.
        Can specify which of the 3 types of fundamental data to convert.
        """

        for stock in self.stocks:
            
            print(stock.ticker)
            stock.convert_fund_to_df(do_income, do_balance, do_cashflow)


       


def main():


    #dr = r'R:\Lab Member Files\Neil Campbell\stocks'
    dr = r'C:\Users\oxide-x240\Documents\Stocks'
    direct = r'C:\Users\oxide-x240\Documents\github\Stocks'
    os.chdir(direct)
    get_from_web = False

    now = datetime.datetime.now()
    print(now.strftime("%m/%d/%Y, %H:%M:%S"))
    #url = 'https://www.ishares.com/us/products/239705/ishares-phlx-semiconductor-etf/1521942788811.ajax?fileType=xls&fileName=iShares-PHLX-Semiconductor-ETF_fund&dataType=fund'

    url = r'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=TWLO&apikey=5ELABCNC7WUW0H21'
    #data = get_fundamental_income("TWLO") 

    #print(data)

    tickers = read_tickers("sp500_tickers.txt")
    print(tickers)
    
    if get_from_web:
        spbasket = StockBasket(tickers)
        spbasket.get_fundamentals(get_income=True,
                                  get_balance=True,
                                  get_cashflow=True)

        with open("stocks", "wb") as stocks_to_write:
            pickle.dump(spbasket, stocks_to_write)

    else:
        with open("stocks", "rb") as stocks_to_write:
            spbasket = pickle.load(stocks_to_write)

        # Uncomment to modify the loaded in StockBasket structure.
        '''
        print("Loaded spbasket")
        spbasket.get_fundamentals(get_income=False,
                                  get_balance=True,
                                  get_cashflow=True)

        print("Downloaded more info")
        with open("stocks", "wb") as stocks_to_write:
            pickle.dump(spbasket, stocks_to_write)

        print("wrote new spbasket")
        '''

    # Do stuff with the StockBasket instance
    
    practice = spbasket.stocks[6].cashflow

    values_df = jm.fundamental_to_df(practice)
    #print(values_df.columns)
    #print(values_df.dtypes)
    print(values_df.head())

    spbasket.convert_fund_to_df(do_income=True,
                                do_balance=True,
                                do_cashflow=True)

    print(spbasket.stocks[6].cashflow_df.head())

    #plt.plot(values_df['capitalExpenditures']/1.e9, 'bo-')
    #plt.show()


if __name__ == '__main__':
    main()
