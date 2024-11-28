import yfinance as yf
import pandas as pd
from typing import Dict, Any

class StockInfo:
    @staticmethod
    def get_basic_info(ticker: str) -> Dict[str, Any]:
        """Get basic information about a stock"""
        stock = yf.Ticker(ticker)
        info = stock.info
        
        return {
            'Name': info.get('longName', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Industry': info.get('industry', 'N/A'),
            'Market Cap': info.get('marketCap', 'N/A'),
            'Current Price': info.get('currentPrice', 'N/A'),
            '52 Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
            '52 Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
            'Volume': info.get('volume', 'N/A'),
            'Average Volume': info.get('averageVolume', 'N/A')
        }

    @staticmethod
    def get_historical_data(ticker: str, period: str) -> pd.DataFrame:
        """Get historical price data for a stock"""
        stock = yf.Ticker(ticker)
        return stock.history(period=period) 