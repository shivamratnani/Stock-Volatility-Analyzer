from setuptools import setup, find_packages

setup(
    name="stock_analyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'yfinance>=0.2.31',
        'pandas>=2.0.0',
        'matplotlib>=3.7.0',
        'numpy>=1.24.0',
        'requests>=2.31.0',
        'pandas_market_calendars>=4.1.4',
        'pytz>=2023.3'
    ],
) 