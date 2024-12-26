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
from src.menu import Menu

class StockAnalysis:
    def __init__(self):
        self.session = self._init_session()
        self.cache = {}
        
        self.batch_size = 50
        self.all_symbols = self._get_all_stock_symbols(False)

    def _init_session(self) -> requests.Session:
        """Initialize a session for faster HTTP requests"""
        session = requests.Session()
        return session

    @lru_cache(maxsize=1)
    def _get_all_stock_symbols(self, analyze_all: bool = False) -> List[str]:
        """get stock symbols based on analysis scope"""
        try:
            if not analyze_all:  # get S&P 500 only
                sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
                sp500_df = pd.read_html(sp500_url)[0]
                symbols = sp500_df['Symbol'].tolist()
                
                # clean symbols
                symbols = [sym.strip().upper() for sym in symbols if isinstance(sym, str)]
                symbols = list(set(symbols))
                # Filter out warrants and special securities
                symbols = [sym for sym in symbols if sym.isalnum() and 
                          not any(x in sym for x in ['W', 'R', 'P', 'Q'])]
                
                if len(symbols) >= 400:
                    return sorted(symbols)
                    
                raise ValueError("Could not fetch S&P 500 list")
                
            else:  # get all NYSE and NASDAQ listings
                try:
                    all_tickers_url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"
                    df = pd.read_csv(all_tickers_url, sep='|', comment='#')
                    
                    # filter active stocks
                    if 'Test Issue' in df.columns:
                        df = df[df['Test Issue'] == 'N']
                    if 'ETF' in df.columns:
                        df = df[df['ETF'] == 'N']
                    
                    # get symbol column
                    symbol_col = [col for col in df.columns if 'symbol' in col.lower()]
                    if symbol_col:
                        symbols = df[symbol_col[0]].tolist()
                    else:
                        raise ValueError("Could not find symbol column in data")
                    
                    # clean symbols and filter out warrants/special securities
                    symbols = [str(sym).strip().upper() for sym in symbols if isinstance(sym, (str, int, float))]
                    symbols = [sym for sym in symbols if sym and sym.isalnum() and 
                              not any(x in sym for x in ['W', 'R', 'P', 'Q'])]
                    symbols = [sym for sym in symbols if not any(x in sym for x in ['TEST', 'DUMMY'])]
                    symbols = list(set(symbols))
                    
                    if len(symbols) > 1000:
                        return sorted(symbols)
                        
                except Exception as e:
                    raise ValueError(f"Error fetching from NASDAQ: {str(e)}")
                    
                raise ValueError("Could not fetch complete stock list")
                
        except Exception as e:
            print(f"\nWarning: Could not fetch stock list: {str(e)}")
            print("Falling back to default S&P 500 stocks...")
            return self._get_default_sp500_symbols()

    def _process_batch(self, symbols: List[str], period: str) -> List[Dict]:
        """process a batch of stock symbols"""
        results = []
        
        for batch in [symbols[i:i + 10] for i in range(0, len(symbols), 10)]:
            try:
                time.sleep(1)  # avoid rate limiting
                
                for symbol in batch:
                    try:
                        clean_symbol = symbol.strip('$').strip()
                        stock = yf.Ticker(clean_symbol, session=self.session)
                        
                        try:
                            hist = stock.history(
                                period=period,
                                interval=self._get_interval(period),
                                timeout=10
                            )
                        except ValueError as e:
                            if "invalid period" in str(e).lower():
                                log_failed_analysis(clean_symbol, period, str(e))
                                continue
                            raise e
                        
                        if hist.empty:
                            error_msg = f"possibly delisted; no price data found (period={period})"
                            log_failed_analysis(clean_symbol, period, error_msg)
                            continue
                            
                        if len(hist) > 1:
                            start_price = float(hist['Close'].iloc[0])
                            end_price = float(hist['Close'].iloc[-1])
                            
                            if start_price > 0 and end_price > 0:
                                percent_change = ((end_price - start_price) / start_price) * 100
                                volume = int(hist['Volume'].mean()) if 'Volume' in hist.columns else 0
                                
                                results.append({
                                    'Symbol': clean_symbol,
                                    'Change%': round(percent_change, 2),
                                    'Start Price': round(start_price, 2),
                                    'End Price': round(end_price, 2),
                                    'Volume': volume
                                })
                                
                    except Exception as e:
                        error_msg = str(e)
                        if "not found" in error_msg.lower() or "delisted" in error_msg.lower():
                            error_msg = f"possibly delisted; no price data found (period={period})"
                        log_failed_analysis(clean_symbol, period, error_msg)
                        continue
                        
            except Exception:
                continue
        
        return results

    def get_gainers_losers(self, period: str, limit: int = 20) -> Tuple[pd.DataFrame, pd.DataFrame, int]:
        """get top gainers and losers for period"""
        try:
            # validate period
            if period not in TIME_PERIODS:
                raise ValueError(f"Invalid period. Must be one of {list(TIME_PERIODS.keys())}")
            
            # Get user preference for analysis scope
            analyze_sp500 = Menu.get_analysis_scope()
            
            # Get symbols based on user preference
            symbols = self._get_all_stock_symbols(analyze_sp500)
            print(f"\nAnalyzing {'S&P 500' if analyze_sp500 else 'all available'} stocks...")
            
            # get all stock data
            total_symbols = len(symbols)
            processed = 0
            results = []
            
            print("\nFetching data...")
            smaller_batches = [symbols[i:i + 10] for i in range(0, len(symbols), 10)]
            
            for batch in smaller_batches:
                results.extend(self._process_batch(batch, period))
                processed += len(batch)
                self._update_progress_bar(processed, total_symbols)
            
            print("\n")  # New line after progress bar
            
            if not results:
                return pd.DataFrame(), pd.DataFrame(), 0
            
            # convert to dataframe
            df = pd.DataFrame(results)
            
            # adjust limit based on available data
            available_stocks = len(df)
            actual_limit = min(limit, available_stocks)
            
            # sort and get top gainers/losers
            gainers = df.nlargest(actual_limit, 'Change%').reset_index(drop=True)
            losers = df.nsmallest(actual_limit, 'Change%').reset_index(drop=True)
            
            return gainers, losers, available_stocks
            
        except Exception as e:
            raise ValueError(f"Error analyzing stocks: {str(e)}")

    def _update_progress_bar(self, current: int, total: int, bar_length: int = 50):
        """Display progress bar"""
        percent = float(current) * 100 / total
        arrow = '-' * int(percent/100 * bar_length - 1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        
        print('\rProgress: [%s%s] %.2f%%' % (arrow, spaces, percent), end='', flush=True)

    def _get_interval(self, period: str) -> str:
        """Get appropriate interval based on period"""
        # Simplified interval mapping
        if period in ['1m', '5m', '15m', '30m', '1h']:
            return '1m'
        elif period in ['12h', '1d']:
            return '5m'
        elif period in ['5d', '1mo']:
            return '1d'
        else:
            return '1d'  # Default interval for longer periods

    @lru_cache(maxsize=100)
    def get_stock_info(self, ticker: str, period: str) -> pd.DataFrame:
        """Get stock information for a specific ticker and period"""
        try:
            stock = yf.Ticker(ticker, session=self.session)
            
            is_intraday = period in INTRADAY_PERIODS
            
            if is_intraday:
                end_time = datetime.now()
                
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
                hist_data = stock.history(
                    period=period,
                    interval=self._get_interval(period)
                )
            
            if hist_data.empty:
                raise ValueError(f"No data available for {ticker}")
            
            summary_data = hist_data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
            
            for col in ['Open', 'High', 'Low', 'Close']:
                summary_data[col] = summary_data[col].round(2)
            
            summary_data['Volume'] = summary_data['Volume'].astype(int)
            
            summary_data['Change %'] = (
                (summary_data['Close'] - summary_data['Open']) / summary_data['Open'] * 100
            ).round(2)
            
            info = stock.info
            
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
        # Get validated and potentially adjusted dates
        start_date, end_date = validate_dates(start_date, end_date)
        
        # Get user preference for analysis scope (True means S&P 500 only)
        analyze_sp500 = Menu.get_analysis_scope()
        
        # Get symbols based on user preference (analyze_sp500=True means analyze S&P 500 only)
        symbols = self._get_all_stock_symbols(analyze_sp500)
        
        print(f"\nAnalyzing {'S&P 500' if analyze_sp500 else 'all available'} stocks...")
        print(f"Period: {start_date} to {end_date}")
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        
        interval = self._determine_interval(delta)
        
        all_data = []
        print(f"\nAnalyzing stocks for period {start_date} to {end_date}...")
        
        for symbol in symbols:
            try:
                stock = yf.Ticker(symbol)
                hist = stock.history(start=start_date, end=end_date, interval=interval)
                if not hist.empty:
                    start_price = hist['Close'].iloc[0]
                    end_price = hist['Close'].iloc[-1]
                    percent_change = ((end_price - start_price) / start_price) * 100
                    
                    all_data.append({
                        'Symbol': symbol,
                        'Change%': round(percent_change, 2),
                        'Start Price': round(start_price, 2),
                        'End Price': round(end_price, 2),
                        'Volume': int(hist['Volume'].mean())
                    })
            except Exception as e:
                print(f"\nWarning: Could not process {symbol}: {str(e)}")
                continue
        
        if not all_data:
            return pd.DataFrame()
        
        result_df = pd.DataFrame(all_data)
        return result_df.sort_values('Change%', ascending=False)

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

    def display_stock_graph(self, ticker: str, period: str) -> pd.DataFrame:
        """Prepare data for visualization"""
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            
            if len(data) >= 20:
                data['SMA_20'] = data['Close'].rolling(window=20).mean()
            if len(data) >= 50:
                data['SMA_50'] = data['Close'].rolling(window=50).mean()
            
            return data
            
        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker}: {str(e)}") 

    def _get_default_sp500_symbols(self) -> List[str]:
        """Return a default list of major S&P 500 stocks if web fetching fails"""
        default_symbols = [
            'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'META', 'BRK-B', 'TSLA', 'UNH', 'XOM',
            'JNJ', 'JPM', 'V', 'PG', 'MA', 'HD', 'CVX', 'ABBV', 'MRK', 'LLY',
            'PEP', 'KO', 'BAC', 'AVGO', 'COST', 'MCD', 'TMO', 'CSCO', 'ACN', 'ABT',
            'DHR', 'WMT', 'CRM', 'LIN', 'VZ', 'CMCSA', 'ADBE', 'TXN', 'PM', 'NEE',
            'BMY', 'RTX', 'ORCL', 'UPS', 'HON', 'QCOM', 'T', 'UNP', 'MS', 'INTC'
        ]
        print("\nUsing default list of top 50 S&P 500 stocks...")
        return default_symbols 