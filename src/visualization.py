# import required modules
import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional

class StockVisualizer:
    def plot_stock_data(self, data: pd.DataFrame, ticker: str, period: str):
        """create stock price chart"""
        # check for data
        if data.empty:
            raise ValueError("No data available to plot")
        
        # create subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])
        
        # plot price data
        ax1.plot(data.index, data['Close'], label='Close Price', color='#1f77b4', linewidth=1)
        
        # add moving averages
        if 'SMA_20' in data.columns:
            ax1.plot(data.index, data['SMA_20'], label='20-day SMA', color='#ff7f0e', linestyle='--', alpha=0.7)
        if 'SMA_50' in data.columns:
            ax1.plot(data.index, data['SMA_50'], label='50-day SMA', color='#2ca02c', linestyle='--', alpha=0.7)
        
        # configure price plot
        ax1.set_title(f'{ticker} Stock Price ({period})', pad=20)
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper left')
        
        # plot volume data
        ax2.bar(data.index, data['Volume'], color='#7f7f7f', alpha=0.5)
        ax2.set_ylabel('Volume')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # format date labels
        plt.gcf().autofmt_xdate()
        
        # adjust layout and display
        plt.tight_layout()
        plt.show()