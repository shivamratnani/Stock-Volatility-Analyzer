from utils.constants import TIME_PERIODS, MenuOptions
from .stock_info import StockInfo
from typing import Optional

class Menu:
    @staticmethod
    def display_main_menu() -> str:
        """Display main menu and get user choice"""
        print("\nStock Data Analysis Tool")
        print("1 --- Get gainers and losers for given time period")
        print("2 --- Get stock data based on your own set time period")
        print("3 --- Get general stock info")
        print("4 --- Show options (Coming Soon)")
        print("5 --- Display graph of set time period")
        print("0 --- Exit")
        return input("\nEnter your choice: ")

    @staticmethod
    def display_time_periods(include_max: bool = False) -> str:
        """Display available time periods and get user choice"""
        print("\nChoose one of the options below:")
        for period, description in TIME_PERIODS.items():
            if period != "max" or include_max:
                print(f"{period} --- {description}")
        print("0 --- Go back")
        return input("\nEnter your choice: ")

    @staticmethod
    def get_stock_ticker() -> str:
        """Get stock ticker from user"""
        return input("Enter the stock ticker symbol (ex. AAPL): ").upper()