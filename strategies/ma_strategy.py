import pandas as pd

def simple_moving_average_strategy(row):
    if not pd.isna(row['UpArrow']):
        return 'buy'
    elif not pd.isna(row['DownArrow']):
        return 'sell'
    else:
        return 'hold'
