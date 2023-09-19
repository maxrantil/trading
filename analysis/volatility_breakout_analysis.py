import sys
import ta
import matplotlib.pyplot as plt
from data_fetcher import fetch_data

# Default to 100 days if no argument is provided
days = 100

# Check if an argument is provided
if len(sys.argv) > 1:
    days = int(sys.argv[1])

def volatility_and_breakouts(df):
    df['UpperBand'], df['MiddleBand'], df['LowerBand'] = ta.volatility.BollingerBands(df['close']).bollinger_hband(), ta.volatility.BollingerBands(df['close']).bollinger_mavg(), ta.volatility.BollingerBands(df['close']).bollinger_lband()
    df['ATR'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
    return df

def plot_volatility_and_breakouts(df):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(12,8))

    plot_start = df['timestamp'].iloc[-days]
    plot_end = df['timestamp'].iloc[-1]

    ax1.plot(df['timestamp'], df['close'], label='Price')
    ax1.plot(df['timestamp'], df['UpperBand'], label='Upper Bollinger Band', linestyle='--')
    ax1.plot(df['timestamp'], df['MiddleBand'], label='Middle Bollinger Band', linestyle='-')
    ax1.plot(df['timestamp'], df['LowerBand'], label='Lower Bollinger Band', linestyle='--')
    ax1.set_xlim([plot_start, plot_end])
    ax1.set_title('Bollinger Bands')
    ax1.legend()

    ax2.plot(df['timestamp'], df['ATR'], label='ATR', color='green')
    ax2.set_xlim([plot_start, plot_end])
    ax2.set_title('Average True Range (ATR)')
    ax2.legend()

    plt.tight_layout()
    plt.show()

# Fetch extra data to ensure Bollinger Bands are calculated from the start of the desired time period
df = fetch_data('BTC/USDT', days + 20)  # Added 20 more days for the calculations to stabilize
indicator_df = volatility_and_breakouts(df)
plot_volatility_and_breakouts(indicator_df)
