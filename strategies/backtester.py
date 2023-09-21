import pandas as pd
from trading.indicators.the_zone_indicator import fetch_btc_data, trend_indicator
from trading.strategies.ma_strategy import simple_moving_average_strategy

# Get data and signals
days = 365  # or any other value you want
indicator_df = trend_indicator(fetch_btc_data(days))

def backtest_strategy(df, strategy_func):
    btc_held = 1.0  # Starting with 1 BTC
    portfolio = 0.0  # USD value
    in_market = True  # Since you're holding BTC at the start

    # Iterate over rows in the dataframe
    for _, row in df.iterrows():
        signal = strategy_func(row)

        if signal == 'buy' and not in_market:
            btc_held = portfolio / row['close']
            portfolio = 0.0
            in_market = True
        elif signal == 'sell' and in_market:
            portfolio = btc_held * row['close']
            btc_held = 0.0
            in_market = False

    # If out of market, convert USD to BTC at end price
    if not in_market:
        btc_held = portfolio / df['close'].iloc[-1]

    return btc_held, in_market

# Assuming you have loaded indicator_df already
btc_end, in_market_status = backtest_strategy(indicator_df, simple_moving_average_strategy)

print(f"Initial BTC: 1.0 BTC")
print(f"Final BTC: {btc_end:.4f} BTC")
if in_market_status:
    print("Currently in the market.")
else:
    print("Currently out of the market.")
