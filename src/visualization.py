import matplotlib.pyplot as plt
import pandas as pd
from typing import Optional

class StockVisualizer:
    def plot_stock_data(self, data: pd.DataFrame, ticker: str, period: str):
        """Create and display a stock price chart"""
        if data.empty:
            raise ValueError("No data available to plot")
        
        # Create figure and subplots with a clean style
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[2, 1])
        
        # Plot price on the first subplot
        ax1.plot(data.index, data['Close'], label='Close Price', color='#1f77b4', linewidth=1)
        
        # Add SMAs if they exist
        if 'SMA_20' in data.columns:
            ax1.plot(data.index, data['SMA_20'], label='20-day SMA', color='#ff7f0e', linestyle='--', alpha=0.7)
        if 'SMA_50' in data.columns:
            ax1.plot(data.index, data['SMA_50'], label='50-day SMA', color='#2ca02c', linestyle='--', alpha=0.7)
        
        # Configure first subplot
        ax1.set_title(f'{ticker} Stock Price ({period})', pad=20)
        ax1.set_ylabel('Price ($)')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper left')
        
        # Plot volume on the second subplot
        ax2.bar(data.index, data['Volume'], color='#7f7f7f', alpha=0.5)
        ax2.set_ylabel('Volume')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Format the date axis
        plt.gcf().autofmt_xdate()  # Angle and align the tick labels so they look better
        
        # Add spacing between subplots
        plt.tight_layout()
        
        # Show the plot
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