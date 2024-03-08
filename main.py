import streamlit as st
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
# SVMBZCBADJX40U62



def ask_user_for_input():
    # ask user for ticker
    ticker = input("Enter the stock ticker symbol (ex. AAPL): ")
    ticker_check = yf.Ticker(ticker)
    while ticker_check.info is None:
        print("Invalid ticker symbol. Please try again.")
        ticker = input("Enter the stock ticker symbol: ")
        ticker_check = yf.Ticker(ticker)

    # ask user for start date & time
    start_date = input("Enter the start date (MM-DD-YYYY): ")
    while len(start_date) != 10:
        print("Invalid date format. Please try again.")
        start_date = input("Enter the start date (MM-DD-YYYY): ")

    start_time = input("Enter the start time or 0 if you would like the most recent data (HH:MM:SS): ")
    while len(start_time) != 8 and start_time != "0":
        print("Invalid time format. Please try again.")
        start_time = input("Enter the start time or 0 if you would like the most recent data (HH:MM:SS): ")

    # ask user for end date & time
    end_date = input("Enter the end date (MM-DD-YYYY): ")
    while len(end_date) != 10:
        print("Invalid date format. Please try again.")
        end_date = input("Enter the end date (MM-DD-YYYY): ")

    end_time = input("Enter the end time or 0 if you would like the most recent data (HH:MM:SS): ")
    while len(end_time) != 8 and end_time != "0":
        print("Invalid time format. Please try again.")
        end_time = input("Enter the end time or 0 if you would like the most recent data (HH:MM:SS): ")

    return ticker, start_date, start_time, end_date, end_time


#Advanced Analytics for AlphaVantage API
# This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, auto-correlation, etc.) for a given time series over a fixed temporal window.
#
#
# API Parameters
# ❚ Required: SYMBOLS
#
# A list of symbols for the calculation. It can be a comma separated list of symbols as a string. Free API keys can specify up to 5 symbols per API request. Premium API keys can specify up to 50 symbols per API request.
#
# ❚ Required: RANGE
#
# This is the date range for the series being requested. By default, the date range is the full set of data for the equity history. This can be further modified by the LIMIT variable.
#
# RANGE can take certain text values as inputs. They are:
#
# full
# {N}day
# {N}week
# {N}month
# {N}year
# For intraday time series, the following RANGE values are also accepted:
#
# {N}minute
# {N}hour
# Aside from the “full” value which represents the entire time series, the other values specify an interval to return the series for as measured backwards from the current date/time.
#
# To specify start & end dates for your analytics calcuation, simply add two RANGE parameters in your API request. For example: RANGE=2023-07-01&RANGE=2023-08-31 or RANGE=2020-12-01T00:04:00&RANGE=2020-12-06T23:59:59 with minute-level precision for intraday analytics. If the end date is missing, the end date is assumed to be the last trading date. In addition, you can request a full month of data by using YYYY-MM format like 2020-12. One day of intraday data can be requested by using YYYY-MM-DD format like 2020-12-06
#
# ❚ Optional: OHLC
#
# This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close.
#
# ❚ Required: INTERVAL
#
# Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY.
#
# ❚ Required: CALCULATIONS
#
# A comma separated list of the analytics metrics you would like to calculate:
#
# MIN: The minimum return (largest negative or smallest positive) for all values in the series
# MAX: The maximum return for all values in the series
# MEAN: The mean of all returns in the series
# MEDIAN: The median of all returns in the series
# CUMULATIVE_RETURN: The total return from the beginning to the end of the series range
# VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalized the output to an annual value. By default, the variance is not annualized.
# STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalized the output to an annual value. By default, the standard deviation is not annualized.
# MAX_DRAWDOWN: Largest peak to trough interval for each symbol in the series range
# HISTOGRAM: For each symbol, place the observed total returns in bins. By default, bins=10. Use HISTOGRAM(bins=20) to specify a custom bin value (e.g., 20).
# AUTOCORRELATION: For each symbol place, calculate the autocorrelation for the given lag (e.g., the lag in neighboring points for the autocorrelation calculation). By default, lag=1. Use AUTOCORRELATION(lag=2) to specify a custom lag value (e.g., 2).
# COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalized the output to an annual value. By default, the covariance is not annualized.
# CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.
# ❚ Required: apikey
#
# API Key: SVMBZCBADJX40U62

def fetch_stock_data(ticker, start_date, end_date, start_time, end_time):
    """
    Fetch historical stock prices from Yahoo Finance.

    :param ticker: Stock ticker symbol.
    :param start_date: Start date for the data in 'YYYY-MM-DD' format.
    :param end_date: End date for the data in 'YYYY-MM-DD' format.
    :param start_time: Start time for the data in 'HH:MM:SS' format.
    :param end_time: End time for the data in 'HH:MM:SS' format.
    :return: DataFrame with historical stock prices.
    """

    # AlphaVantage API
    url = "https://alphavantageapi.co/timeseries/analytics?SYMBOLS=" + ticker + "&RANGE=" + start_date + "&RANGE=" + end_date + "&INTERVAL=" + "DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo"
    r = requests.get(url)
    data = r.json()

    # yFinance API
    stock_yFinance = yf.Ticker(ticker)
    data_yFinance = stock_yFinance.history(start=start_date, end=end_date)
    return data



def print_stock_data(data):
    """
    Print the stock data to the console.

    :param data: DataFrame with stock price data.
    """
    print(data)

def display_stock_data(data):
    st.title("Real-time " + data.info + " Stock Prices")
    ticker = data.ticker

def calculate_volatility(data):
    """
    Calculate and return the annualized volatility of stock.

    :param data: DataFrame with stock price data.
    :return: Annualized volatility as a float.
    """
    # Calculate daily returns
    data['Daily Return'] = data['Close'].pct_change()

    # Calculate daily returns
    data['Daily Return'] = data['Close'].pct_change()

    # Calculate daily volatility
    daily_volatility = data['Daily Return'].std()

    # Annualize daily volatility
    annualized_volatility = daily_volatility * (252 ** 0.5)  # Assuming 252 trading days in a year
    return annualized_volatility


# main function
def main():
    # while True:


    ticker = "AAPL"  # Apple Inc.
    start_date = "2023-01-01"
    end_date = "2023-12-31"

    stock_data = fetch_stock_data(ticker, start_date, end_date)
    print_stock_data(stock_data)
    volatility = calculate_volatility(stock_data)
    print(f"The annualized volatility of {ticker} from {start_date} to {end_date} is: {volatility:.2%}")


# Example usage
ticker = "AAPL"  # Apple Inc.
start_date = "2023-01-01"
end_date = "2023-12-31"

stock_data = fetch_stock_data(ticker, start_date, end_date)
volatility = calculate_volatility(stock_data)
print(f"The annualized volatility of {ticker} from {start_date} to {end_date} is: {volatility:.2%}")
