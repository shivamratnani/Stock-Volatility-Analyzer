import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock prices from Yahoo Finance.

    :param ticker: Stock ticker symbol.
    :param start_date: Start date for the data in 'YYYY-MM-DD' format.
    :param end_date: End date for the data in 'YYYY-MM-DD' format.
    :return: DataFrame with historical stock prices.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data


def calculate_volatility(data):
    """
    Calculate and return the annualized volatility of stock.

    :param data: DataFrame with stock price data.
    :return: Annualized volatility as a float.
    """
    # Calculate daily returns
    data['Daily Return'] = data['Close'].pct_change()

    # Calculate daily volatility
    daily_volatility = data['Daily Return'].std()

    # Annualize daily volatility
    annualized_volatility = daily_volatility * (252 ** 0.5)  # Assuming 252 trading days in a year
    return annualized_volatility


# Example usage
ticker = "AAPL"  # Apple Inc.
start_date = "2023-01-01"
end_date = "2023-12-31"

stock_data = fetch_stock_data(ticker, start_date, end_date)
volatility = calculate_volatility(stock_data)
print(f"The annualized volatility of {ticker} from {start_date} to {end_date} is: {volatility:.2%}")
