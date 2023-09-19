import pandas as pd
import matplotlib.pyplot as plt
import ccxt
import matplotlib
matplotlib.use('TkAgg')
import sys

if len(sys.argv) > 1:
    try:
        days = int(sys.argv[1])
    except ValueError:
        print("Please provide a valid number for days.")
        sys.exit(1)
else:
    days = 100  # Default to 100 days if no argument is provided

def fetch_btc_data(days=100):
    binance = ccxt.binance()
    ohlcv = binance.fetch_ohlcv('BTC/USDT', '1d', limit=days)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def trend_indicator(df):
    df['MA10'] = df['close'].rolling(window=10).mean()
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()

    df['UpArrow'] = None
    df['DownArrow'] = None

    for i in range(len(df)):
        if df['MA10'].iloc[i] > df['MA50'].iloc[i] and df['MA20'].iloc[i] > df['MA50'].iloc[i]:
            if df['close'].iloc[i] > df['open'].iloc[i] and df['close'].iloc[i] > df['MA10'].iloc[i] and df['close'].iloc[i] < df['MA20'].iloc[i]:
                df['UpArrow'].iloc[i] = df['low'].iloc[i]

        elif df['MA10'].iloc[i] < df['MA50'].iloc[i] and df['MA20'].iloc[i] < df['MA50'].iloc[i]:
            if df['close'].iloc[i] < df['open'].iloc[i] and df['close'].iloc[i] < df['MA10'].iloc[i] and df['close'].iloc[i] > df['MA20'].iloc[i]:
                df['DownArrow'].iloc[i] = df['high'].iloc[i]

    return df

def plot_data(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df['timestamp'], df['close'], label='BTC/USDT', color='blue')
    plt.plot(df['timestamp'], df['MA10'], label='MA10', color='orange')
    plt.plot(df['timestamp'], df['MA20'], label='MA20', color='green')
    plt.plot(df['timestamp'], df['MA50'], label='MA50', color='red')
    plt.scatter(df['timestamp'], df['UpArrow'], color='lime', label='Up Trend', marker='^')
    plt.scatter(df['timestamp'], df['DownArrow'], color='red', label='Down Trend', marker='v')
    plt.title("BTC/USDT Price and Trend Indicator")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

df = fetch_btc_data(days)
indicator_df = trend_indicator(df)
plot_data(indicator_df)
