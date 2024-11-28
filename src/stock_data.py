import yfinance as yf
import pandas as pd
from datetime import datetime
from utils.validators import validate_ticker, validate_dates

class StockData:
    def __init__(self):
        self.data = None
        
    def fetch_data(self, ticker: str, period: str = None, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Fetch stock data based on period or date range"""
        validate_ticker(ticker)
        
        if start_date and end_date:
            validate_dates(start_date, end_date)
            self.data = yf.download(ticker, start=start_date, end=end_date)
        else:
            self.data = yf.download(ticker, period=period)
            
        return self.data
        
    def get_gainers_losers(self, period: str, limit: int = 20) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Get top gainers and losers for the specified period"""
        # Implementation for fetching gainers and losers
        pass 