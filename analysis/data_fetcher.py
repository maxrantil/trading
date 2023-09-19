import pandas as pd
import ccxt
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds, consider adjusting based on the API's rate limits

def fetch_data(symbol='BTC/USDT', days=100):
    binance = ccxt.binance()
    retries = 0

    while retries < MAX_RETRIES:
        try:
            ohlcv = binance.fetch_ohlcv(symbol, '1d', limit=days)

            # Ensure data is valid
            if not ohlcv or len(ohlcv) == 0:
                logging.warning(f"No data returned from the API for {symbol}. Retrying...")
                retries += 1
                time.sleep(RETRY_DELAY)
                continue

            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df

        except ccxt.RequestTimeout as e:
            logging.warning(f"Timeout error: {e}. Retrying in {RETRY_DELAY} seconds...")
            retries += 1
            time.sleep(RETRY_DELAY)

        except ccxt.ExchangeNotAvailable as e:
            logging.warning(f"Exchange not available: {e}. Retrying in {RETRY_DELAY} seconds...")
            retries += 1
            time.sleep(RETRY_DELAY)

        except ccxt.DDoSProtection as e:
            logging.warning(f"DDoS protection error: {e}. Retrying in {RETRY_DELAY} seconds...")
            retries += 1
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"An error occurred: {e}. Exiting...")
            break

    logging.error(f"Failed to fetch data for {symbol} after {MAX_RETRIES} retries.")
    return None
