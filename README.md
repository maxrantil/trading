## TO START
source trading_env/bin/activate
pip install -r requirements.txt

## TO END
deactivate

## The Zone Indicator
##- This indicator provides insights based on Moving Averages to potentially identify market trends. It plots the BTC/USDT price, 10-day, 20-day, and 50-day moving averages. Trending situations are highlighted with up and down arrows.

python indicators/the_zone_indicator.py 7     # For 7 days
python indicators/the_zone_indicator.py 30    # For 30 days
python indicators/the_zone_indicator.py 365   # For 365 days


## Trend Confirmation with Momentum
##- Moving Average (e.g., EMA50 or EMA100): To identify the overall trend. A rising EMA suggests an uptrend, and a falling EMA indicates a downtrend.
##- MACD: To confirm the trend direction. If MACD is above its signal line and above zero, it confirms the uptrend. If it's below its signal line and below zero, it confirms the downtrend.
##- RSI: To identify overbought or oversold conditions. Values above 70 suggest potential overbought conditions (might reverse down), and values below 30 suggest potential oversold conditions (might reverse up).

python indicators/trend_momentum_analysis.py 30
python indicators/trend_momentum_analysis.py 180
python indicators/trend_momentum_analysis.py 365


## Volatility and Breakouts
##- Bollinger Bands: These give a sense of the volatility in the market. A narrowing of bands suggests decreased volatility (potential breakout incoming), while bands moving apart indicate increased volatility.
##- Volume: To confirm the breakout. An increase in volume during the breakout suggests it's more valid.
##- Average True Range (ATR): Provides a sense of volatility and can be used to set stop-loss levels.

python indicators/volatility_breakout_analysis.py 30
python indicators/volatility_breakout_analysis.py 90
python indicators/volatility_breakout_analysis.py 180


## Trend Strength and Money Flow
##- Moving Averages (e.g., EMA50 and EMA200): A common strategy is to look for the crossover of these averages. EMA50 crossing above EMA200 is a "golden cross" (bullish), and EMA50 crossing below EMA200 is a "death cross" (bearish).
##- On Balance Volume (OBV): If the OBV is rising while the price is in an uptrend, it confirms the trend. If OBV is falling while the price is in a downtrend, it also confirms the trend. Divergences between price and OBV can signal potential reversals.
##- Chaikin Money Flow (CMF): It indicates buying and selling pressure. A positive CMF indicates buying pressure (bullish), while a negative CMF indicates selling pressure (bearish).

python indicators/trend_strength_moneyflow_analysis.py 250
python indicators/trend_strength_moneyflow_analysis.py 500
python indicators/trend_strength_moneyflow_analysis.py 1000
