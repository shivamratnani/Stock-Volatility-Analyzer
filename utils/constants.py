from typing import Dict

class MenuOptions:
    GAINERS_LOSERS = "1"
    CUSTOM_PERIOD = "2"
    STOCK_INFO = "3"
    OPTIONS = "4"
    GRAPH = "5"
    EXIT = "0"

# Separate dictionaries for intraday and regular periods
INTRADAY_PERIODS: Dict[str, str] = {
    "1m": "Last 1 minute of data",
    "5m": "Last 5 minutes of data with 1 minute increments",
    "15m": "Last 15 minutes of data with 1 minute increments",
    "30m": "Last 30 minutes of data with 1 minute increments",
    "1h": "Last 1 hour of data with 1 minute increments",
    "12h": "Last 12 hours of data with 5 minute increments",
}

REGULAR_PERIODS: Dict[str, str] = {
    "1d": "Last 1 day of data with 1 hour increments",
    "5d": "Last 5 days of data with 1 day increments",
    "1mo": "Last 1 month of data with 1 day increments",
    "3mo": "Last 3 months of data with 1 day increments",
    "6mo": "Last 6 months of data with 1 day increments",
    "1y": "Last 1 year of data with 1 day increments",
    "2y": "Last 2 years of data with 1 day increments",
    "5y": "Last 5 years of data with 1 day increments",
    "10y": "Last 10 years of data with 1 day increments",
    "ytd": "Year to date data with 1 day increments",
    "max": "Maximum available data"
}

# Combined periods for display
TIME_PERIODS: Dict[str, str] = {**INTRADAY_PERIODS, **REGULAR_PERIODS}