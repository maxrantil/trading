import sys
import matplotlib.pyplot as plt
import ta
from data_fetcher import fetch_data

# Default to 100 days if no argument is provided
days = 100

# Check if an argument is provided
if len(sys.argv) > 1:
    days = int(sys.argv[1])

def trend_strength_and_money_flow(df):
    df['EMA50'] = ta.trend.ema_indicator(df['close'], window=50)
    df['EMA200'] = ta.trend.ema_indicator(df['close'], window=200)
    df['OBV'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
    df['CMF'] = ta.volume.ChaikinMoneyFlowIndicator(df['high'], df['low'], df['close'], df['volume']).chaikin_money_flow()
    return df

def plot_trend_strength_and_money_flow(df):
    fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(12,9))

    plot_start = df['timestamp'].iloc[200]  # This is the 200th day
    plot_end = df['timestamp'].iloc[-1]

    ax1.plot(df['timestamp'], df['close'], label='Price')
    ax1.plot(df['timestamp'], df['EMA50'], label='EMA50', linestyle='--')
    ax1.plot(df['timestamp'], df['EMA200'], label='EMA200', linestyle='-')
    ax1.set_xlim([plot_start, plot_end])
    ax1.set_title('Price, EMA50 & EMA200')
    ax1.legend()

    ax2.plot(df['timestamp'], df['OBV'], label='On Balance Volume (OBV)', color='purple')
    ax2.set_xlim([plot_start, plot_end])
    ax2.set_title('On Balance Volume (OBV)')
    ax2.legend()

    ax3.plot(df['timestamp'], df['CMF'], label='Chaikin Money Flow (CMF)', color='brown')
    ax3.axhline(0, linestyle='--', color='grey')
    ax3.set_xlim([plot_start, plot_end])
    ax3.set_title('Chaikin Money Flow (CMF)')
    ax3.legend()

    plt.tight_layout()
    plt.show()

# Fetch additional 200 days for EMA200 calculation
df = fetch_data('BTC/USDT', days + 200)
indicator_df = trend_strength_and_money_flow(df)
plot_trend_strength_and_money_flow(indicator_df)
