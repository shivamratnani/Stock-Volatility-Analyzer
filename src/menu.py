# import required modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import TIME_PERIODS, MenuOptions
from src.stock_info import StockInfo
from typing import Optional
from utils.validators import is_market_open, get_last_trading_day
from utils.constants import TIME_PERIODS, INTRADAY_PERIODS, REGULAR_PERIODS

class Menu:
    @staticmethod
    def display_main_menu() -> str:
        """show main menu options"""
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
        """show available time periods"""
        print("\nChoose one of the options below:")
        
        # Check if market is currently open
        market_open = is_market_open()
        
        for period, description in TIME_PERIODS.items():
            # Skip intraday periods if market is closed
            if not market_open and period in INTRADAY_PERIODS:
                continue
            
            if period != "max" or include_max:
                print(f"{period} --- {description}")
                
        if not market_open:
            print("\nNote: Intraday options are hidden because the market is currently closed.")
            
        print("0 --- Go back")
        choice = input("\nEnter your choice: ")
        return choice

    @staticmethod
    def get_analysis_scope() -> bool:
        """get user preference for analysis scope"""
        while True:
            choice = input("\nAnalyze all S&P 500 stocks for faster analysis? (y/n): ").lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("Please enter 'y' for S&P 500 stocks or 'n' for all stocks")

    @staticmethod
    def get_stock_ticker() -> str:
        """get ticker from user"""
        return input("Enter the stock ticker symbol (ex. AAPL): ").upper()