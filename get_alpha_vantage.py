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


def get_fundamental_income(ticker):
    """
    Get the Income Statment information going back 5 years for the given ticker.
    This communicates with the Alpha Vantage API, so you need an internet connection.
    It returns the JSON version. Because API calls are limited, we isolate this 
    function, then save with pickle, and format wiht format_fundamental_income().
    """
    #
    base = r"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol="
    end = "&apikey=5ELABCNC7WUW0H21"
    url = base + ticker.upper() + end
    #print(url)
    resp = requests.get(url)
    data = resp.json()

    return data



def main():


    #dr = r'R:\Lab Member Files\Neil Campbell\stocks'
    dr = r'C:\Users\oxide-x240\Documents\Stocks'
    os.chdir(dr)

    now = datetime.datetime.now()
    print(now.strftime("%m/%d/%Y, %H:%M:%S"))
    #url = 'https://www.ishares.com/us/products/239705/ishares-phlx-semiconductor-etf/1521942788811.ajax?fileType=xls&fileName=iShares-PHLX-Semiconductor-ETF_fund&dataType=fund'

    url = r'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=TWLO&apikey=5ELABCNC7WUW0H21'
    #urlretrieve(url, dr + 'SOXX_holdings.xls')
    #resp = requests.get(url)
    data = get_fundamental_income("TWLO") 

    print('I like Silicon')
    #output = open('test.xls', 'wb')
    #output.write(resp.content)
    #output.close()

    #data = resp.json()
    print(data)
    #etfile = pd.read_excel('test.xls')
    #print etfile.head()

    #df = pd.read_csv(dr + 'SOXX_holdings.xls', skiprows=37, engine='python')
    #print df.head()

if __name__ == '__main__':
    main()
