from typing import Tuple, List, Dict, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from functools import lru_cache
import requests
from datetime import datetime, timedelta
from utils.validators import validate_ticker, validate_dates
from utils.constants import TIME_PERIODS, INTRADAY_PERIODS, REGULAR_PERIODS

class StockAnalysis:
    def __init__(self):
        self.session = self._init_session()
        self.cache = {}
        self.batch_size = 50  # Reduced batch size for better reliability

    def _init_session(self) -> requests.Session:
        """Initialize a session for faster HTTP requests"""
        session = requests.Session()
        return session

    @lru_cache(maxsize=1)
    def _get_all_stock_symbols(self) -> List[str]:
        """Cache the stock symbols to avoid repeated downloads"""
        try:
            # Download from a reliable source (you might want to store this locally)
            url = "https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv"
            df = pd.read_csv(url)
            return df['Ticker'].tolist()
        except:
            # Fallback to a smaller list for testing
            return ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

    def _process_batch(self, symbols: List[str], period: str) -> List[Dict]:
        """Process a batch of symbols"""
        results = []
        
        # Create a single yfinance download for the batch
        data = yf.download(
            tickers=symbols,
            period=period,
            interval=self._get_interval(period),
            group_by='ticker',
            threads=True,
            progress=False,
            session=self.session
        )

        # Process each symbol in the batch
        for symbol in symbols:
            try:
                if isinstance(data, pd.DataFrame):
                    # Single symbol case
                    hist = data
                else:
                    # Multiple symbols case
                    hist = data[symbol]

                if not hist.empty:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    percent_change = ((end_price - start_price) / start_price) * 100
                    results.append({
                        'Symbol': symbol,
                        'Change%': round(percent_change, 2),
                        'Start Price': round(start_price, 2),
                        'End Price': round(end_price, 2),
                        'Volume': int(hist['Volume'].mean())
                    })
            except Exception:
                continue

        return results

    def get_gainers_losers(self, period: str, limit: int = 20) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Get top gainers and losers for the specified period"""
        if period not in TIME_PERIODS:
            raise ValueError(f"Invalid period. Must be one of {list(TIME_PERIODS.keys())}")
        
        print(f"\nAnalyzing stocks for {TIME_PERIODS[period]}...")
        
        # List of major stocks to analyze
        symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "JPM", "V", "WMT",
            "PG", "XOM", "BAC", "MA", "DIS", "NFLX", "CSCO", "PFE", "INTC", "VZ",
            "KO", "PEP", "CMCSA", "ADBE", "CRM", "ABT", "TMO", "ACN", "NKE", "MCD",
            "AMD", "PYPL", "QCOM", "COST", "UNH", "CVX", "T", "ORCL", "LLY", "MRK"
        ]
        
        # Download data for all symbols at once
        try:
            data = yf.download(
                tickers=symbols,
                period=period,
                interval=self._get_interval(period),
                group_by='ticker',
                progress=False
            )
            
            all_changes = []
            
            for symbol in symbols:
                try:
                    if len(data.columns.levels) > 1:  # Multiple symbols
                        hist = data[symbol]
                    else:  # Single symbol
                        hist = data
                        
                    if not hist.empty and len(hist) > 1:
                        start_price = hist['Close'].iloc[0]
                        end_price = hist['Close'].iloc[-1]
                        
                        if start_price > 0 and end_price > 0:
                            percent_change = ((end_price - start_price) / start_price) * 100
                            volume = int(hist['Volume'].mean())
                            
                            all_changes.append({
                                'Symbol': symbol,
                                'Change%': round(percent_change, 2),
                                'Start Price': round(start_price, 2),
                                'End Price': round(end_price, 2),
                                'Volume': volume
                            })
                            
                except Exception as e:
                    print(f"\nWarning: Could not process {symbol}: {str(e)}")
                    continue
            
            if not all_changes:
                return pd.DataFrame(), pd.DataFrame()
            
            # Convert to DataFrame
            changes_df = pd.DataFrame(all_changes)
            
            # Sort by Change%
            gainers = changes_df.nlargest(limit, 'Change%')
            losers = changes_df.nsmallest(limit, 'Change%')
            
            return gainers, losers
            
        except Exception as e:
            print(f"\nError downloading data: {str(e)}")
            return pd.DataFrame(), pd.DataFrame()

    def _get_interval(self, period: str) -> str:
        """Get appropriate interval based on period"""
        interval_map = {
            "1m": "1m",
            "5m": "1m",
            "15m": "1m",
            "30m": "1m",
            "1h": "1m",
            "12h": "5m",
            "1d": "1m",
            "5d": "5m",
            "1mo": "1h",
            "3mo": "1d",
            "6mo": "1d",
            "1y": "1d",
            "2y": "1wk",
            "5y": "1wk",
            "10y": "1mo",
            "ytd": "1d",
            "max": "1mo"
        }
        return interval_map.get(period, "1d")

    @lru_cache(maxsize=100)
    def get_stock_info(self, ticker: str, period: str) -> pd.DataFrame:
        """Get stock information for a specific ticker and period"""
        try:
            stock = yf.Ticker(ticker, session=self.session)
            
            # Check if intraday data is being requested
            is_intraday = period in INTRADAY_PERIODS
            
            if is_intraday:
                # For intraday data, we need to calculate the start and end times
                end_time = datetime.now()
                
                # Calculate start time based on period
                if period == "1m":
                    start_time = end_time - timedelta(minutes=1)
                    interval = "1m"
                elif period == "5m":
                    start_time = end_time - timedelta(minutes=5)
                    interval = "1m"
                elif period == "15m":
                    start_time = end_time - timedelta(minutes=15)
                    interval = "1m"
                elif period == "30m":
                    start_time = end_time - timedelta(minutes=30)
                    interval = "1m"
                elif period == "1h":
                    start_time = end_time - timedelta(hours=1)
                    interval = "1m"
                else:  # 12h
                    start_time = end_time - timedelta(hours=12)
                    interval = "5m"
                
                # Try to get intraday data
                try:
                    hist_data = stock.history(
                        start=start_time,
                        end=end_time,
                        interval=interval
                    )
                    
                    if hist_data.empty:
                        raise ValueError(
                            f"Intraday data (period: {period}) is not available for {ticker}. "
                            "Try using a longer time period."
                        )
                
                except Exception as e:
                    raise ValueError(
                        f"Error fetching intraday data: {str(e)}. "
                        "Intraday data might not be available for this stock."
                    )
            
            else:
                # Regular period data
                hist_data = stock.history(
                    period=period,
                    interval=self._get_interval(period)
                )
            
            if hist_data.empty:
                raise ValueError(f"No data available for {ticker}")
            
            # Format the historical data
            summary_data = hist_data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            
            # Round numeric columns to 2 decimal places
            for col in ['Open', 'High', 'Low', 'Close']:
                summary_data[col] = summary_data[col].round(2)
            
            # Format volume as integer
            summary_data['Volume'] = summary_data['Volume'].astype(int)
            
            # Add percentage change column
            summary_data['Change %'] = (
                (summary_data['Close'] - summary_data['Open']) / summary_data['Open'] * 100
            ).round(2)
            
            # Get current stock info for header
            info = stock.info
            
            # Print header with current information
            print(f"\nCurrent Information for {ticker.upper()}")
            print("-" * 80)
            print(f"Current Price: ${info.get('currentPrice', 'N/A'):,.2f}")
            print(f"Market Cap: ${info.get('marketCap', 0):,.2f}")
            print(f"52 Week Range: ${info.get('fiftyTwoWeekLow', 'N/A'):,.2f} - ${info.get('fiftyTwoWeekHigh', 'N/A'):,.2f}")
            print(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
            print(f"Dividend Yield: {info.get('dividendYield', 0) * 100:.2f}%")
            print("-" * 80)
            print(f"\nHistorical Data ({TIME_PERIODS[period]}):")
            
            return summary_data
            
        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker}: {str(e)}")

    def get_custom_period_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Get stock data for custom date range"""
        validate_dates(start_date, end_date)
        
        # Calculate appropriate interval based on date range
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        
        interval = self._determine_interval(delta)
        
        all_data = []
        for symbol in self.all_symbols:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(start=start_date, end=end_date, interval=interval)
                if not hist.empty:
                    hist['Symbol'] = symbol
                    all_data.append(hist)
            except Exception as e:
                continue
                
        return pd.concat(all_data) if all_data else pd.DataFrame()

    def _determine_interval(self, delta: timedelta) -> str:
        """Determine appropriate interval based on date range"""
        days = delta.days
        
        if days <= 1:
            return "1m"
        elif days <= 7:
            return "5m"
        elif days <= 30:
            return "1h"
        elif days <= 90:
            return "1d"
        elif days <= 365:
            return "1d"
        else:
            return "1wk"

    def display_stock_graph(self, ticker: str, period: str):
        """Prepare data for visualization"""
        data = self.get_stock_info(ticker, period)
        return data[['Open', 'High', 'Low', 'Close', 'Volume']] 