# Stock Analysis Tool

A Python-based tool for analyzing stock market data and visualizing market trends. This application provides real-time and historical stock data analysis with an interactive command-line interface.

## Features

* **Market Gainers and Losers Analysis**
  - Analyze top gainers and losers for any specified time period
  - Support for both S&P 500 stocks and broader market analysis
  - Flexible time periods from 1-minute intervals to 10-year historical data
  - Configurable limit for number of stocks to display

* **Custom Period Analysis**
  - Analyze stock performance between any two dates
  - Automatic adjustment to last trading day if end date falls on non-trading day
  - Dynamic interval selection based on date range

* **Stock Information**
  - Access basic company information including sector and industry
  - View key metrics like market cap, current price, and trading volumes
  - Display 52-week price ranges
  - Show average trading volumes

* **Technical Analysis**
  - Generate price charts with customizable time periods
  - Display moving averages (20-day and 50-day SMA when applicable)
  - Volume analysis and visualization
  - Interactive charts with matplotlib

* **Market-Aware Features**
  - Automatic detection of market trading hours
  - Intraday data options only available during market hours
  - Fallback to last trading day for non-trading periods

## Requirements

- Python 3.7+
- yfinance
- pandas
- matplotlib
- pandas_market_calendars
- pytz

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shivamratnani/Stock-Volatility-Analyzer.git
cd stock-analysis-tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the main program:
```bash
python main.py
```

### Main Menu Options

1. Get gainers and losers for given time period
2. Get stock data based on your own set time period
3. Get general stock info
4. Show options (Coming Soon)
5. Display graph of set time period
0. Exit

### Time Periods Available

#### Intraday Periods (During Market Hours)
- 1m: Last 1 minute of data
- 5m: Last 5 minutes of data
- 15m: Last 15 minutes of data
- 30m: Last 30 minutes of data
- 1h: Last 1 hour of data
- 12h: Last 12 hours of data

#### Regular Periods
- 1d: Last 1 day of data
- 5d: Last 5 days of data
- 1mo: Last 1 month of data
- 3mo: Last 3 months of data
- 6mo: Last 6 months of data
- 1y: Last 1 year of data
- 2y: Last 2 years of data
- 5y: Last 5 years of data
- 10y: Last 10 years of data
- ytd: Year to date data
- max: Maximum available data

## Error Handling

- Failed analysis attempts are logged to 'failed_analysis.txt'
- Automatic retry mechanism for API calls
- Graceful handling of market closures and invalid dates
- Comprehensive input validation for tickers and dates

## Data Sources

- Stock data is fetched using the Yahoo Finance API via yfinance
- S&P 500 constituent list is retrieved from Wikipedia
- Market calendar data from NYSE calendar

## Notes

- Intraday data options are only available during market hours
- The tool automatically adjusts to the last trading day when analyzing non-trading days
- Default analysis is limited to S&P 500 stocks for optimal performance, with an option to analyze all available stocks
- For stability, the tool implements rate limiting and error handling when fetching data
- GUI is coming soon!!
