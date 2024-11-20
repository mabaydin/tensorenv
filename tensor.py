import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import yfinance as yf
import pandas_market_calendars as mcal
from plotly.offline import init_notebook_mode, plot
init_notebook_mode(connected=True)
-  -  
#Defining market capital
def create_market_cal(start, end):
    nyse = mcal.get_calendar('NYSE')
    schedule = nyse.schedule(stocks_start, stocks_end)
    market_cal = mcal.date_range(schedule, frequency='1D')
    market_cal = market_cal.tz_localize(None)
    market_cal = [i.replace(hour=0) for i in market_cal]
    return market_cal


def get_data(stocks, start, end):
    def data(ticker):
        df = yf.download(ticker, start=start, end=(end + datetime.timedelta(days=1)))
        df['symbol'] = ticker
        df.index = pd.to_datetime(df.index)
        return df
    datas = map(data, stocks)
    return(pd.concat(datas, keys=stocks, names=['Ticker', 'Date'], sort=True))


def get_benchmark(benchmark, start, end):
    benchmark = get_data(benchmark, start, end)
    benchmark = benchmark.drop(['symbol'], axis=1)
    benchmark.reset_index(inplace=True)
    return benchmark

portfolio_df = pd.read_csv('stock_transactions.csv')
portfolio_df['Open date'] = pd.to_datetime(portfolio_df['Open date'])
symbols = portfolio_df.Symbol.unique()
stocks_start = datetime.datetime(2017, 9, 1)
stocks_end = datetime.datetime(2020, 4, 7)
daily_adj_close = get_data(symbols, stocks_start, stocks_end)
daily_adj_close = daily_adj_close[['Close']].reset_index()
daily_benchmark = get_benchmark(['SPY'], stocks_start, stocks_end)
daily_benchmark = daily_benchmark[['Date', 'Close']]
market_cal = create_market_cal(stocks_start, stocks_end)

