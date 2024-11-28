import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional

class StockVisualizer:
    def plot_stock_data(self, data: pd.DataFrame, ticker: str, period: str):
        """Create and display a stock price chart"""
        plt.figure(figsize=(12, 6))
        
        # Plot price
        plt.subplot(2, 1, 1)
        plt.plot(data.index, data['Close'], label='Close Price', color='blue')
        plt.plot(data.index, data.get('SMA_20', []), label='20-day SMA', color='red', linestyle='--')
        plt.plot(data.index, data.get('SMA_50', []), label='50-day SMA', color='green', linestyle='--')
        plt.title(f'{ticker} Stock Price ({period})')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        
        # Plot volume
        plt.subplot(2, 1, 2)
        plt.bar(data.index, data['Volume'], color='gray', alpha=0.5)
        plt.title('Volume')
        plt.ylabel('Volume')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()
        
    def plot_gainers_losers(self, gainers: pd.DataFrame, losers: pd.DataFrame):
        """Create a comparison chart of top gainers and losers"""
        plt.figure(figsize=(15, 7))
        
        # Plot gainers
        plt.subplot(1, 2, 1)
        plt.barh(gainers['Symbol'], gainers['Change%'], color='green')
        plt.title('Top Gainers')
        plt.xlabel('Percent Change')
        
        # Plot losers
        plt.subplot(1, 2, 2)
        plt.barh(losers['Symbol'], losers['Change%'], color='red')
        plt.title('Top Losers')
        plt.xlabel('Percent Change')
        
        plt.tight_layout()
        plt.show() 