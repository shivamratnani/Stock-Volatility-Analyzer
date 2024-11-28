from src.menu import Menu
from src.stock_data import StockData
from src.stock_analysis import StockAnalysis
from src.visualization import StockVisualizer
from utils.constants import MenuOptions, TIME_PERIODS
from utils.validators import validate_ticker, validate_dates
from datetime import datetime
import pandas as pd
import time
from typing import Dict

def display_dataframe(df: pd.DataFrame, title: str = ""):
    """Helper function to display dataframes in a formatted way"""
    if df.empty:
        print("\nNo data available")
        return
        
    if title:
        print(f"\n{title}")
    print("-" * 80)
    
    # Format the display for gainers/losers
    if 'Change%' in df.columns:
        df = df.copy()
        df['Change%'] = df['Change%'].apply(lambda x: f"{x:+.2f}%")
        df['Start Price'] = df['Start Price'].apply(lambda x: f"${x:,.2f}")
        df['End Price'] = df['End Price'].apply(lambda x: f"${x:,.2f}")
        df['Volume'] = df['Volume'].apply(lambda x: f"{x:,}")
    
    print(df.to_string(index=False))
    print("-" * 80)

def main():
    menu = Menu()
    stock_analysis = StockAnalysis()
    visualizer = StockVisualizer()
    
    while True:
        try:
            choice = menu.display_main_menu()
            
            if choice == MenuOptions.EXIT:
                print("Thank you for using the Stock Analysis Tool!")
                return
                
            if choice == MenuOptions.GAINERS_LOSERS:
                period = menu.display_time_periods()
                if period == "0":
                    continue
                
                try:
                    print("\nFetching data... This might take a few minutes.")
                    start_time = time.time()
                    gainers, losers = stock_analysis.get_gainers_losers(period)
                    elapsed_time = time.time() - start_time
                    
                    if gainers.empty or losers.empty:
                        print("\nNo data available for the selected period")
                    else:
                        print(f"\nAnalysis completed in {elapsed_time:.2f} seconds")
                        display_dataframe(gainers, "Top 20 Gainers")
                        display_dataframe(losers, "Top 20 Losers")
                except ValueError as e:
                    print(f"\nError: {e}")
                    
            elif choice == MenuOptions.CUSTOM_PERIOD:
                while True:
                    try:
                        start_date = input("Enter start date (YYYY-MM-DD): ")
                        end_date = input("Enter end date (YYYY-MM-DD): ")
                        validate_dates(start_date, end_date)
                        break
                    except ValueError as e:
                        print(f"Error: {e}")
                        continue
                
                print("\nFetching data... This might take a few minutes.")
                data = stock_analysis.get_custom_period_data(start_date, end_date)
                display_dataframe(data, "Custom Period Analysis")
                
            elif choice == MenuOptions.STOCK_INFO:
                while True:
                    ticker = input("Enter the stock ticker symbol (ex. AAPL): ").strip()
                    if ticker.lower() == '0':
                        break
                    
                    try:
                        if validate_ticker(ticker):
                            period = menu.display_time_periods(include_max=True)
                            if period == "0":
                                continue
                            
                            data = stock_analysis.get_stock_info(ticker, period)
                            display_dataframe(data)
                            break
                            
                    except ValueError as e:
                        print(f"Error: {e}")
                        print("Enter 0 to go back or try another ticker symbol")
                        continue
                
            elif choice == MenuOptions.OPTIONS:
                print("\nOptions trading features coming soon!")
                
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
            
            if choice != MenuOptions.EXIT:
                input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            if choice != MenuOptions.EXIT:
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
