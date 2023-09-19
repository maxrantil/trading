import pandas as pd
import ta
import ccxt
import matplotlib.pyplot as plt
import argparse
from data_fetcher import fetch_data

# Constants
DEFAULT_DAYS = 100
RSI_UPPER_THRESHOLD = 70
RSI_LOWER_THRESHOLD = 30

def get_days_from_args():
    """Parse and return number of days from command line arguments."""
    parser = argparse.ArgumentParser(description='Fetch and analyze BTC/USDT data for a number of days.')
    parser.add_argument('days', type=int, nargs='?', default=DEFAULT_DAYS,
                        help=f'Number of days to fetch and analyze (default: {DEFAULT_DAYS} days)')
    args = parser.parse_args()
    return args.days

days = get_days_from_args()
df = fetch_data('BTC/USDT', days)
print(len(df))

def trend_confirmation_with_momentum(df):
    """Add the EMA50, MACD, MACD Signal Line, and RSI indicators to the dataframe."""
    df['EMA50'] = ta.trend.ema_indicator(df['close'], window=50)

    macd_indicator = ta.trend.MACD(df['close'])
    df['MACD'] = macd_indicator.macd()
    df['Signal_Line'] = macd_indicator.macd_signal()

    df['RSI'] = ta.momentum.RSIIndicator(df['close']).rsi()

    # Drop rows with NaN values
    df.dropna(inplace=True)
    print(df.isna().sum())
    return df

def plot_trend_confirmation_with_momentum(df):
    """Plot the price along with the EMA50, MACD, Signal Line, and RSI indicators."""
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(12,9))

    ax1.plot(df['timestamp'], df['close'], label='Price')
    ax1.plot(df['timestamp'], df['EMA50'], label='EMA50', linestyle='--')
    ax1.set_title('Price & EMA50')
    ax1.legend()

    ax2.plot(df['timestamp'], df['MACD'], label='MACD')
    ax2.plot(df['timestamp'], df['Signal_Line'], label='Signal Line', color='red')
    ax2.axhline(0, linestyle='--', color='grey')
    ax2.set_title('MACD and Signal Line')
    ax2.legend()

    ax3.plot(df['timestamp'], df['RSI'], label='RSI', color='orange')
    ax3.axhline(0, linestyle='--', alpha=0.5, color='gray')
    ax3.axhline(20, linestyle='--', alpha=0.5, color='red')
    ax3.axhline(30, linestyle='--', alpha=0.5, color='orange')
    ax3.axhline(70, linestyle='--', alpha=0.5, color='orange')
    ax3.axhline(80, linestyle='--', alpha=0.5, color='red')
    ax3.axhline(100, linestyle='--', alpha=0.5, color='gray')
    ax3.set_title('RSI')
    ax3.legend()

    plt.tight_layout()
    plt.show()

indicator_df = trend_confirmation_with_momentum(df)
plot_trend_confirmation_with_momentum(indicator_df)
