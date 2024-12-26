# import required modules
from src.menu import Menu
from src.stock_data import StockData
from src.stock_analysis import StockAnalysis
from src.visualization import StockVisualizer
from utils.constants import MenuOptions, TIME_PERIODS
from src.utils import display_dataframe, validate_dates
from datetime import datetime
import pandas as pd
import time
from typing import Dict
from utils.validators import validate_ticker, validate_dates
from src.stock_info import StockInfo

def display_dataframe(df: pd.DataFrame, title: str = ""):
    """format and display dataframes"""
    # check if data exists
    if df.empty:
        print("\nNo data available")
        return
        
    # print title if provided
    if title:
        print(f"\n{title}")
    print("-" * 80)
    
    # format numbers for display
    if 'Change%' in df.columns:
        df = df.copy()
        df['Change%'] = df['Change%'].apply(lambda x: f"{x:+.2f}%")
        df['Start Price'] = df['Start Price'].apply(lambda x: f"${x:,.2f}")
        df['End Price'] = df['End Price'].apply(lambda x: f"${x:,.2f}")
        df['Volume'] = df['Volume'].apply(lambda x: f"{x:,}")
    
    print(df.to_string(index=False))
    print("-" * 80)

def log_failed_analysis(ticker: str, period: str, error_msg: str):
    """Log failed stock analysis attempts"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("failed_analysis.txt", "a") as f:
        if not f.tell():  # If file is empty, write header
            f.write(f"Analysis Date: {timestamp}\n")
            f.write(f"Period: {period}\n\n")
        f.write(f"{ticker}: {error_msg}\n")

def main():
    # initialize main objects
    menu = Menu()
    stock_analysis = StockAnalysis()
    visualizer = StockVisualizer()
    
    # main program loop
    while True:
        try:
            choice = menu.display_main_menu()
            
            # handle exit
            if choice == MenuOptions.EXIT:
                print("Thank you for using the Stock Analysis Tool!")
                return
            
            # handle gainers/losers analysis    
            if choice == MenuOptions.GAINERS_LOSERS:
                period = menu.display_time_periods()
                if period == "0":
                    continue
                
                while True:
                    try:
                        limit = input("\nHow many top gainers/losers would you like to see? (min = 1, default = 20): ").strip()
                        if not limit:  # If user just hits enter, use default
                            limit = 20
                            break
                        limit = int(limit)
                        if 1 <= limit <= 100:
                            break
                        print("Please enter a number between 1 and 100")
                    except ValueError:
                        print("Please enter a valid number")
                
                analyze_sp500 = menu.get_analysis_scope()
                try:
                    print("\nFetching data... This might take a few minutes.")
                    start_time = time.time()
                    gainers, losers, available_stocks = stock_analysis.get_gainers_losers(period, limit, analyze_sp500)
                    elapsed_time = time.time() - start_time
                    
                    if gainers.empty or losers.empty:
                        print("\nNo data available for the selected period")
                    else:
                        actual_limit = min(limit, available_stocks)
                        if actual_limit < limit:
                            print(f"\nNote: Only {available_stocks} stocks available for analysis. Showing all available stocks.")
                        
                        print(f"\nAnalysis completed in {elapsed_time:.2f} seconds")
                        display_dataframe(gainers, f"Top {actual_limit} Gainers")
                        display_dataframe(losers, f"Top {actual_limit} Losers")
                except ValueError as e:
                    error_msg = str(e)
                    print(f"\nError: {error_msg}")
                    log_failed_analysis("Analysis", period, error_msg)
                except Exception as e:
                    error_msg = str(e)
                    print(f"\nAn unexpected error occurred: {error_msg}")
                    log_failed_analysis("Analysis", period, error_msg)
            
            # handle custom period analysis        
            elif choice == MenuOptions.CUSTOM_PERIOD:
                while True:
                    try:
                        analyze_all = menu.get_analysis_scope()
                        start_date = input("Enter start date (YYYY-MM-DD): ")
                        end_date = input("Enter end date (YYYY-MM-DD): ")
                        validate_dates(start_date, end_date)
                        break
                    except ValueError as e:
                        print(f"Error: {e}")
                        continue
                
                print("\nFetching data... This might take a few minutes.")
                data = stock_analysis.get_custom_period_data(start_date, end_date, analyze_all)
                display_dataframe(data, "Custom Period Analysis")
            
            # handle stock info display    
            elif choice == MenuOptions.STOCK_INFO:
                ticker = input("Enter the stock ticker symbol (ex. AAPL): ").upper()
                try:
                    validate_ticker(ticker)
                    info = StockInfo.get_basic_info(ticker)
                    
                    print(f"\nStock Information for {ticker}")
                    print("-" * 80)
                    for key, value in info.items():
                        if key == 'Market Cap' and isinstance(value, (int, float)):
                            print(f"{key}: ${value:,.2f}")
                        elif key in ['Current Price', '52 Week High', '52 Week Low'] and isinstance(value, (int, float)):
                            print(f"{key}: ${value:.2f}")
                        elif key in ['Volume', 'Average Volume'] and isinstance(value, (int, float)):
                            print(f"{key}: {value:,}")
                        else:
                            print(f"{key}: {value}")
                    print("-" * 80)
                except ValueError as e:
                    error_msg = str(e)
                    print(f"Error: {error_msg}")
                    log_failed_analysis(ticker, "N/A", error_msg)
                except Exception as e:
                    error_msg = str(e)
                    print(f"Error fetching stock information: {error_msg}")
                    log_failed_analysis(ticker, "N/A", error_msg)
            
            # handle options menu (placeholder)        
            elif choice == MenuOptions.OPTIONS:
                print("\nOptions trading features coming soon!")
            
            # handle graph display    
            elif choice == MenuOptions.GRAPH:
                while True:
                    ticker = input("Enter the stock ticker symbol (ex. AAPL): ").upper()
                    try:
                        validate_ticker(ticker)
                        break
                    except ValueError as e:
                        print(f"Error: {e}")
                        continue
                
                period = menu.display_time_periods()
                if period == "0":
                    continue
                    
                try:
                    data = stock_analysis.display_stock_graph(ticker, period)
                    visualizer.plot_stock_data(data, ticker, period)
                except Exception as e:
                    print(f"Error creating graph: {e}")
            
            else:
                print("Invalid option. Please try again.")
            
            # wait for user input before continuing
            if choice != MenuOptions.EXIT:
                input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            if choice != MenuOptions.EXIT:
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()