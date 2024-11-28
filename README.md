# Stock Volatility Analyzer

A Python-based tool for analyzing stock market data, tracking volatility, and visualizing market trends in real-time. This application provides comprehensive stock analysis tools including historical data analysis, price tracking, and graphical visualizations.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Code Examples](#code-examples)
- [Output Examples](#output-examples)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Functionality
- Real-time stock data analysis
- Historical price tracking
- Top gainers and losers identification
- Custom date range analysis
- Stock price visualization with charts

### Time Period Options

#### Intraday Analysis:
- 1 minute intervals
- 5 minute intervals
- 15 minute intervals
- 30 minute intervals
- 1 hour intervals
- 12 hour intervals

#### Regular Periods:
- Daily (1d, 5d)
- Monthly (1mo, 3mo, 6mo)
- Yearly (1y, 2y, 5y, 10y)
- Year to date (ytd)
- Maximum available data

### Data Visualization
- Price charts with moving averages
- Volume analysis
- Comparative analysis tools
- Gainers/Losers visualization

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)
- Internet connection for real-time data

## Installation

### Clone the Repository:
```bash
git clone https://github.com/yourusername/Stock-Volatility-Analyzer.git
cd Stock-Volatility-Analyzer
```

### Set Up Virtual Environment:

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Dependencies
- yfinance
- pandas>=2.0.0
- matplotlib>=3.7.0
- numpy>=1.24.0

## Usage

### Starting the Program
```bash
python main.py
```

### Main Menu Options

1. **Get Gainers and Losers (Option 1)**
   - View top performing and underperforming stocks
   - Choose from various time periods
   - See percentage changes and volume data

2. **Custom Period Analysis (Option 2)**
   - Enter custom date ranges
   - Get detailed historical data
   - Format: YYYY-MM-DD

3. **General Stock Info (Option 3)**
   - Basic stock information
   - Current market data
   - Historical performance

4. **Options Trading Features (Option 4)**
   - Coming Soon

5. **Graph Display (Option 5)**
   - Interactive price charts
   - Volume visualization
   - Technical indicators

## Code Examples

### Fetching Stock Data
```python
from src.stock_analysis import StockAnalysis

analyzer = StockAnalysis()
data = analyzer.get_stock_info("AAPL", "1d")
```

### Creating Visualizations
```python
from src.visualization import StockVisualizer

visualizer = StockVisualizer()
visualizer.plot_stock_data(data, "AAPL", "1d")
```

## Output Examples

### Stock Information Display
```
Current Information for AAPL
--------------------------------------------------------------------------------
Current Price: $234.93
Market Cap: $3,551,155,000,000.00
52 Week Range: $189.99 - $234.93
P/E Ratio: 28.5
Dividend Yield: 0.54%
```

### Gainers/Losers Analysis
```
Top 20 Gainers
--------------------------------------------------------------------------------
Symbol Change%    Start Price    End Price       Volume
TSLA   +88.34%   $176.75       $332.89         91,534,656
ORCL   +46.76%   $124.49       $182.70         8,466,684
```

## Troubleshooting

### Common Issues

1. **No Data Available**
   - Check internet connection
   - Verify stock ticker exists
   - Ensure market hours for intraday data

2. **API Rate Limits**
   - Wait a few minutes between requests
   - Use longer time intervals
   - Reduce batch size for multiple stocks

3. **Installation Issues**
   - Update pip: `pip install --upgrade pip`
   - Check Python version compatibility
   - Verify all dependencies are installed

## Development

### Setting Up Development Environment

1. **Clone and Install:**
```bash
git clone https://github.com/yourusername/Stock-Volatility-Analyzer.git
cd Stock-Volatility-Analyzer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. **Docker Support:**
```bash
docker build -t stock-analyzer .
docker run -it stock-analyzer
```

### Project Structure
```
Stock-Volatility-Analyzer/
├── src/
│   ├── __init__.py
│   ├── stock_analysis.py
│   ├── stock_data.py
│   ├── stock_info.py
│   ├── menu.py
│   └── visualization.py
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   └── validators.py
├── main.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 guidelines
- Include docstrings for all functions
- Add type hints
- Write unit tests for new features

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

For additional support or questions, please open an issue on the GitHub repository.
