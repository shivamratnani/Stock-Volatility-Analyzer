from datetime import datetime
import yfinance as yf
import time

def validate_ticker(ticker: str) -> bool:
    """Validate if ticker exists with retry mechanism"""
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty")
        
    ticker = ticker.upper()
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            # Try to get basic info first
            info = stock.info
            
            # Check if we got valid data back
            if info and isinstance(info, dict):
                # Check for essential fields that should exist for valid tickers
                if any([
                    info.get('regularMarketPrice'),
                    info.get('currentPrice'),
                    info.get('ask'),
                    info.get('bid')
                ]):
                    return True
            
            time.sleep(retry_delay)
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            continue
    
    raise ValueError(f"Invalid ticker symbol: {ticker}")

def validate_dates(start_date: str, end_date: str) -> bool:
    """Validate date format and range"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start >= end:
            raise ValueError("Start date must be before end date")
            
        if end > datetime.now():
            raise ValueError("End date cannot be in the future")
            
        return True
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD format. {str(e)}") 