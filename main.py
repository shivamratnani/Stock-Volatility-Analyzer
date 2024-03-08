import streamlit as st
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# SVMBZCBADJX40U62


def ask_user_for_input():
    # ask user for ticker
    ticker_input = input("Enter the stock ticker symbol (ex. AAPL): ")
    ticker_check = yf.Ticker(ticker_input)
    while ticker_check.info is None:
        print("Invalid ticker symbol. Please try again.")
        ticker_input = input("Enter the stock ticker symbol: ")
        ticker_check = yf.Ticker(ticker_input)

    # ask user for start date & time
    print(
        "Please enter the start date and time for the data you would like to analyze. Enter today, yesterday, week, month, year, or all for the entire dataset. Additionally, you can enter a specific date and time in the format MM-DD-YYYY HH:MM:SS.")
    start_date_input = input("Enter the start date (MM-DD-YYYY): ")

    # remove spaces
    start_date_input = start_date_input.replace(" ", "")

    # add support for today, yesterday, week, month, year, all

    # start date - mm-dd-yyyy format
    if start_date_input == "today":
        start_date_input = datetime.today().strftime('%m-%d-%Y')
    elif start_date_input == "yesterday":
        start_date_input = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')
    elif start_date_input == "week":
        start_date_input = (datetime.today() - timedelta(days=7)).strftime('%m-%d-%Y')
    elif start_date_input == "month":
        start_date_input = (datetime.today() - timedelta(days=30)).strftime('%m-%d-%Y')
    elif start_date_input == "year":
        start_date_input = (datetime.today() - timedelta(days=365)).strftime('%m-%d-%Y')
    elif start_date_input == "all":
        start_date_input = datetime.today().strftime('%m-%d-%Y')

    # end date



    while len(
        start_date_input) != 10:
        print("Invalid date format. Please try again.")
        start_date_input = input("Enter the start date (MM-DD-YYYY): ")

    start_time_input = input("Enter the start time or 0 if you would like the most recent data (HH:MM:SS): ")
    while len(start_time_input) != 8 and start_time_input != "0":
        print("Invalid time format. Please try again.")
        start_time_input = input("Enter the start time or 0 if you would like the most recent data (HH:MM:SS): ")

    # ask user for end date & time
    end_date_input = input("Enter the end date (MM-DD-YYYY): ")

    # remove spaces
    end_date_input = end_date_input.replace(" ", "")

    # add support for today, yesterday, week, month, year, all
    if end_date_input == "today":
        end_date_input = datetime.today().strftime('%m-%d-%Y')
    elif end_date_input == "yesterday":
        end_date_input = (datetime.today() - timedelta(days=1)).strftime('%m-%d-%Y')
    elif end_date_input == "week":
        end_date_input = (datetime.today() - timedelta(days=7)).strftime('%m-%d-%Y')
    elif end_date_input == "month":
        end_date_input = (datetime.today() - timedelta(days=30)).strftime('%m-%d-%Y')
    elif end_date_input == "year":
        end_date_input = (datetime.today() - timedelta(days=365)).strftime('%m-%d-%Y')
    elif end_date_input == "all":
        end_date_input = "01-01-1970"



    while len(end_date_input) != 10:
        print("Invalid date format. Please try again.")
        end_date_input = input("Enter the end date (MM-DD-YYYY): ")

    end_time = input("Enter the end time or 0 if you would like the most recent data (HH:MM:SS): ")
    while len(end_time) != 8 and end_time != "0":
        print("Invalid time format. Please try again.")
        end_time = input("Enter the end time or 0 if you would like the most recent data (HH:MM:SS): ")

    return ticker_input, start_date_input, start_time_input, end_date_input, end_time


def calculate_days(start_date, end_date):
    date_format = "%m-%d-%Y"
    start_datetime = datetime.strptime(start_date, date_format)
    end_datetime = datetime.strptime(end_date, date_format)
    amount_of_days = end_datetime - start_datetime
    return amount_of_days


# Advanced Analytics for AlphaVantage API
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

def fetch_stock_data(ticker_fetch, start_data_fetch, end_date_fetch):
    """
    Fetch historical stock prices from Yahoo Finance.

    :param ticker_fetch: Stock ticker symbol.
    :param start_data_fetch: Start date for the data in 'YYYY-MM-DD' format.
    :param end_date_fetch: End date for the data in 'YYYY-MM-DD' format.
    :param start_time_fetch: Start time for the data in 'HH:MM:SS' format.
    :param end_time_fetch: End time for the data in 'HH:MM:SS' format.
    :return: DataFrame with historical stock prices.
    """

    interval = "15min"

    # Calculate the amount of days between the start and end date
    amount_of_days = calculate_days(start_data_fetch, end_date_fetch)
    print(amount_of_days)

    if amount_of_days == 0:
        interval = "1min"

    if amount_of_days.days >= 365:
        interval = "DAILY"

    # AlphaVantage API
    # CALCULATIONS=MIN,MAX,MEAN,MEDIAN,CUMULATIVE_RETURN,VARIANCE,STDDEV,MAX_DRAWDOWN,HISTOGRAM,AUTOCORRELATION,COVARIANCE,CORRELATION&apikey=SVMBZCBADJX40U62
    url = "https://alphavantageapi.co/timeseries/analytics?SYMBOLS=" + ticker_fetch + "&RANGE=" + start_data_fetch + "&RANGE=" + end_date_fetch + "&OHLC=close&INTERVAL=" + interval + "&CALCULATIONS=CUMULATIVE_RETURN&apikey=SVMBZCBADJX40U62"
    r = requests.get(url)
    data = r.json()

    # print the data
    print(data)

    # yFinance API
    # tock_yFinance = yf.Ticker(ticker_fetch)
    # data_yFinance = stock_yFinance.history(start=start_data_fetch, end=end_date_fetch)
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


# main function
if __name__ == "__main__":
    while True:
        print("Welcome to the Stock Data Analysis Tool!")
        print("This tool allows you to fetch and analyze stock data.")

        # ask user for input
        ticker, start_date, start_time, end_date, end_time = ask_user_for_input()

        # fetch stock data
        stock_data = fetch_stock_data(ticker, start_date, end_date)

        # print stock data
        print_stock_data(stock_data)
