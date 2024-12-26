# import required modules
from datetime import datetime, timedelta
import yfinance as yf
import time
import pandas_market_calendars as mcal
import pytz

def validate_ticker(ticker: str) -> bool:
    """check if ticker exists"""
    # check for empty ticker
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty")
        
    ticker = ticker.upper()
    max_retries = 3
    retry_delay = 1  # seconds
    
    # try multiple times to validate ticker
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # check if valid data returned
            if info and isinstance(info, dict):
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

def validate_dates(start_date: str, end_date: str) -> tuple[str, str]:
    """Validate and adjust dates for stock data availability."""
    try:
        # convert strings to dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        current = datetime.now()
        
        # check if end date is a market day
        if not is_market_open(end):
            last_trading_day = get_last_trading_day(end)
            end = last_trading_day
            end_date = end.strftime('%Y-%m-%d')
            print(f"\nNote: Adjusted end date to last trading day: {end_date}")
        
        # check date logic
        if start >= end:
            raise ValueError("Start date must be before end date")
            
        if end > current:
            raise ValueError("End date cannot be in the future")
        
        return start_date, end_date
        
    except ValueError as e:
        raise ValueError(f"Invalid date format or range. {str(e)}")

def is_market_open(check_date: datetime = None) -> bool:
    """Check if the market is open on a given date"""
    nyse = mcal.get_calendar('NYSE')
    et_tz = pytz.timezone('US/Eastern')
    
    if check_date is None:
        check_date = datetime.now(et_tz)
    elif check_date.tzinfo is None:
        check_date = et_tz.localize(check_date)
    
    # Get market schedule for the date
    schedule = nyse.schedule(
        start_date=check_date.date(),
        end_date=check_date.date()
    )
    
    # Check if market is open on this date
    if schedule.empty:
        return False
        
    # For current date, also check current time
    if check_date.date() == datetime.now(et_tz).date():
        market_open = schedule.iloc[0]['market_open'].to_pydatetime()
        market_close = schedule.iloc[0]['market_close'].to_pydatetime()
        return market_open <= check_date <= market_close
        
    return True

def get_last_trading_day(check_date: datetime = None) -> datetime:
    """Get the most recent trading day"""
    nyse = mcal.get_calendar('NYSE')
    et_tz = pytz.timezone('US/Eastern')
    
    if check_date is None:
        check_date = datetime.now(et_tz)
    elif check_date.tzinfo is None:
        check_date = et_tz.localize(check_date)
    
    # Look back up to 10 days to find last trading day
    start_date = check_date.date() - timedelta(days=10)
    schedule = nyse.schedule(start_date=start_date, end_date=check_date.date())
    
    if not schedule.empty:
        return schedule.iloc[-1]['market_close'].to_pydatetime()
    
    raise ValueError("Could not determine last trading day")