import streamlit as st
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# SVMBZCBADJX40U62

def get_stock_ticker():
    """
    Prompt the user to input a stock ticker symbol and validate it.

    This function prompts the user to input a stock ticker symbol and validates it using the yfinance library.
    If the ticker symbol is invalid, the user is asked to try again until a valid symbol is entered.
    The function returns the validated ticker symbol.

    Returns:
    str: The validated stock ticker symbol.

    Example:
    >>> get_stock_ticker()
    Enter the stock ticker symbol (ex. AAPL): AAPL
    'AAPL'
    """
    ticker = input("Enter the stock ticker symbol (ex. AAPL): ")

    # Check if the ticker symbol is valid
    if yf.Ticker(ticker).info is None:
        print("Invalid ticker symbol. Please try again.")
        # If the ticker symbol is invalid, ask the user to input again
        get_stock_ticker()

    # Return the validated ticker symbol
    return ticker


def get_ticker_and_period(choice):
    """
    Get the stock ticker symbol and time period from the user.

    This function prompts the user to input a stock ticker symbol and validates it using the yfinance library.
    If the ticker symbol is invalid, the user is asked to try again until a valid symbol is entered.
    Depending on the user's choice, the function either calls the given_period function or the customized_period function to get the time period.

    Parameters:
    choice (str): The user's choice. If "1", the given_period function is called. If "2", the customized_period function is called.

    Returns:
    tuple: A tuple containing the start date, end date, period, and interval. The start date and end date are set to "0" if the given_period function is called. The period and interval are set to 0 if the customized_period function is called.
    """

    # ask user for ticker
    ticker_input = input("Enter the stock ticker symbol (ex. AAPL): ")
    ticker_check = yf.Ticker(ticker_input)
    while ticker_check.info is None:
        print("Invalid ticker symbol. Please try again.")
        ticker_input = input("Enter the stock ticker symbol: ")
        ticker_check = yf.Ticker(ticker_input)

    if choice == "1":
        period, interval = given_period()
        return ticker_input, "0", "0", period, interval
    elif choice == "2":
        start_date, end_date = customized_period()
        return ticker_input, start_date, end_date, 0, 0


def given_period():
    """
    Ask the user to input a given time period.

    This function prompts the user to input a time period from a list of valid options.
    If the user enters an invalid time period, they are asked to try again until a valid period is entered.
    The function also sets the interval based on the entered period.

    Returns:
    tuple: A tuple containing the period and interval.
    """

    # ask user for given period
    interval = input(
        "Enter 1m, 5m, 15m, 30m, 1h, 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, or max to specify the time period: ")
    period = interval

    while period not in ["1m", "5m", "15m", "30m", "1h", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y",
                           "ytd", "max"]:
        print("Invalid time period. Please try again.")
        interval = input(
            "Enter 1m, 5m, 15m, 30m, 1h, 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, or max to specify the time period.")
        period = interval

    if period == "1m" or "5m" or "15m" or "30m" or "1h":
        period = "1d"
        return period, interval
    elif period == "1d":
        interval = "1m"
    elif period == "5d":
        interval = "5m"
    elif period == "1mo":
        interval = "15m"
    elif period == "3mo" or "6mo" or "1y" or "2y" or "5y" or "10y" or "ytd" or "max":
        interval = "1d"

    return period, interval


def customized_period():
    """
    Ask the user to input a start and end date.

    This function prompts the user to input a start and end date in 'YYYY-MM-DD' format.
    The user is also informed that they can enter 0 if they have no preference for the start and end time.
    The function returns the start and end date as a tuple.

    Returns:
    tuple: A tuple containing the start and end date in 'YYYY-MM-DD' format.

    Example:
    >>> customized_period()
    Enter the start date in 'YYYY-MM-DD' format: 2020-01-01
    Enter the end date in 'YYYY-MM-DD' format: 2021-01-01
    Enter 0 if no preference for start and end time.
    ('2020-01-01', '2021-01-01')
    """

    start_date_input = input("Enter the start date in 'YYYY-MM-DD' format: ")
    end_date_input = input("Enter the end date in 'YYYY-MM-DD' format: ")
    print("Enter 0 if no preference for start and end time.")

    return start_date_input, end_date_input


def calculate_days(start_date, end_date):
    """
    Calculate the number of days between two dates.

    This function takes two dates as input in the format 'MM-DD-YYYY' and returns the number of days between them.
    The returned value is a datetime.timedelta object which represents the difference between two dates.

    Parameters:
    start_date (str): The start date in 'MM-DD-YYYY' format.
    end_date (str): The end date in 'MM-DD-YYYY' format.

    Returns:
    datetime.timedelta: The number of days between the start and end date.

    Example:
    >>> calculate_days('01-01-2020', '01-01-2021')
    datetime.timedelta(days=366)
    """

    date_format = "%m-%d-%Y"
    if start_date == "0":
        start_datetime = datetime.now()
    else:
        start_datetime = datetime.strptime(start_date, date_format)
    if end_date == "0":
        end_datetime = datetime.now()
    else:
        end_datetime = datetime.strptime(end_date, date_format)
    amount_of_days = end_datetime - start_datetime
    return amount_of_days


def convert_time_to_period(days):
    """
    Convert a given number of days to a corresponding time period.

    This function takes a number of days as input and returns a string representing the corresponding time period.
    The time period is determined based on the following ranges:
    - 1 day or less: "1d"
    - 2 to 5 days: "5d"
    - 6 to 30 days: "1mo"
    - 31 to 90 days: "3mo"
    - 91 to 180 days: "6mo"
    - 181 to 365 days: "1y"
    - 366 to 730 days: "2y"
    - 731 to 1825 days: "5y"
    - 1826 to 3650 days: "10y"
    - 3651 days or more: "max"
    Note: For a period of 365.25 days, the function returns "ytd" considering it as a leap year.

    Parameters:
    days (int): The number of days.

    Returns:
    str: A string representing the corresponding time period.

    Example:
    >>> convert_time_to_period(400)
    '2y'
    """

    if days <= 1:
        return "1d"
    elif days <= 5:
        return "5d"
    elif days <= 30:
        return "1mo"
    elif days <= 90:
        return "3mo"
    elif days <= 180:
        return "6mo"
    elif days <= 365:
        return "1y"
    elif days <= 730:
        return "2y"
    elif days <= 1825:
        return "5y"
    elif days <= 3650:
        return "10y"
    elif days <= 365.25:  # considering leap year
        return "ytd"
    else:
        return "max"


def fetch_stock_info(ticker):
    """
    Fetch stock information from Yahoo Finance.

    This function uses the yfinance library to fetch stock information for a given ticker symbol.
    The information is returned as a dictionary.

    Parameters:
    ticker (str): The ticker symbol for the stock.

    Returns:
    dict: A dictionary containing the stock information.

    Example:
    >>> fetch_stock_info("AAPL")
    {'shortName': 'Apple Inc.', 'longName': 'Apple Inc.', 'sector': 'Technology', ...}

    Note:
    The returned dictionary contains many keys. The exact keys returned may vary depending on the stock.
    """

    # Create a Ticker object for the given ticker symbol
    stock_yFinance = yf.Ticker(ticker)

    # Fetch the stock information
    info = stock_yFinance.info

    # Prompt the user to select the information they want to see
    print("Enter 1 for forwardPE, 2 for dividendRate, 3 for marketCap, 4 for volume, 5 for averageVolume (24hrs), 6 for averageVolume10days, 7 for dayHigh, 8 for dayLow, 9 for fiftyTwoWeekHigh, 10 for fiftyTwoWeekLow, -1 to exit.")
    needed_info = input("Enter the information you want: ")

    # Depending on the user's choice, print the corresponding information
    if needed_info == "1":
        print(info["forwardPE"])
    elif needed_info == "2":
        print(info["dividendRate"])
    elif needed_info == "3":
        print(info["marketCap"])
    elif needed_info == "4":
        print(info["volume"])
    elif needed_info == "5":
        print(info["averageVolume"])
    elif needed_info == "6":
        print(info["averageVolume10days"])
    elif needed_info == "7":
        print(info["dayHigh"])
    elif needed_info == "8":
        print(info["dayLow"])
    elif needed_info == "9":
        print(info["fiftyTwoWeekHigh"])
    elif needed_info == "10":
        print(info["fiftyTwoWeekLow"])
    elif needed_info == "-1":
        return info

    # Return the stock information
    return info


def fetch_stock_options(ticker):
    """
    Fetch and display stock options for a given ticker symbol.

    This function fetches the stock options for a given ticker symbol using the yfinance library.
    The user is prompted to input an expiration date for the options and whether they want to see puts or calls.
    The function then prints the corresponding options to the console.

    Parameters:
    ticker (yfinance.Ticker object): The ticker symbol for the stock.

    Example:
    >>> fetch_stock_options(yf.Ticker("AAPL"))
    Enter the expiration date for the options (ex: 2020-07-24): 2020-07-24
    Enter 1 for puts and 2 for calls: 1
    [prints puts options]
    """
    # Get the options for the given ticker symbol
    ticker_options = ticker.options
    print(ticker_options)

    # Prompt the user to input an expiration date for the options
    option_date = input("Enter the expiration date for the options (ex: 2020-07-24): ")
    while option_date not in ticker_options:
        print("Invalid expiration date. Please try again.")
        option_date = input("Enter the expiration date for the options: ")

    # Prompt the user to choose between puts and calls
    option_choice = input("Enter 1 for puts and 2 for calls: ")
    while option_choice not in ["1", "2"]:
        print("Invalid choice. Please try again.")
        option_choice = input("Enter 1 for puts and 2 for calls: ")

    # Print the corresponding options
    if option_choice == "1":
        puts = ticker.option_chain(option_date).puts
        print(puts)
    elif option_choice == "2":
        calls = ticker.option_chain(option_date).calls
        print(calls)

    return ticker_options


def fetch_stock_data(ticker_fetch, start_data_fetch, end_date_fetch, period, interval):
    """
    Fetch historical stock prices from Yahoo Finance.

    :param ticker_fetch: Stock ticker symbol.
    :param start_data_fetch: Start date for the data in 'YYYY-MM-DD' format.
    :param end_date_fetch: End date for the data in 'YYYY-MM-DD' format.
    :param interval: Time interval for the data.
    :return: DataFrame with historical stock prices.
    """

    # Calculate the amount of days between the start and end date
    amount_of_days = calculate_days(start_data_fetch, end_date_fetch)
    if interval == 0:
        period = convert_time_to_period(amount_of_days.days)
        if 0 <= amount_of_days.days < 7:
            interval = "1m"
        elif 7 <= amount_of_days.days < 30:
            interval = "5m"
        elif amount_of_days.days < 60:
            interval = "15m"
    print(amount_of_days)
    print(period)
    print(interval)

    # yFinance API
    stock_yFinance = yf.Ticker(ticker_fetch)
    data_yFinance = yf.download(ticker_fetch, period=period, interval=interval)
    data = data_yFinance

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

    # user choice
    choice = 9

    while choice != 0:
        print("Welcome to the Stock Data Analysis Tool!")
        print("This tool allows you to fetch and analyze stock data.")

        # Ask user what they want to do
        choice = input(
            "Enter 1 to get gainers and losers for given period, 2 to get stock data for customized period, 3 to get stock info, 4 to show options, 5 to display graph, or 0 to exit: ")

        # get stock ticker and period
        if choice == "1" or choice == "2":
            ticker, start_date, end_date, period, interval = get_ticker_and_period(choice)
            data = fetch_stock_data(ticker, start_date, end_date, period, interval)
            print_stock_data(data)

        elif choice == "3":
            ticker = get_stock_ticker()
            stock_info = fetch_stock_info(ticker)
            print(stock_info)
        elif choice == "4":
            ticker = get_stock_ticker()
            stock_yFinance = yf.Ticker(ticker)
            ticker_options = fetch_stock_options(stock_yFinance)

        # fetch stock data
        stock_data = fetch_stock_data

        # print stock data
        print_stock_data(stock_data)
