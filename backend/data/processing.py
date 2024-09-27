import pandas as pd
import numpy as np
from backend.data.ingestion import fetch_kline_data
from backend.data.storage import save_kline_data, get_kline_data
from functools import lru_cache

def fetch_and_store_kline_data(symbol, interval, limit):
    # Fetch the latest data point
    end_time = int(pd.Timestamp.now().timestamp() * 1000)
    start_time = end_time - (limit * get_interval_milliseconds(interval))
    
    data = fetch_kline_data(symbol, interval, start_time, end_time)
    if data:
        # Convert the data to the expected format
        formatted_data = [
            {
                'openTime': int(item[0]),
                'open': float(item[1]),
                'high': float(item[2]),
                'low': float(item[3]),
                'close': float(item[4]),
                'volume': float(item[5]),
                'closeTime': int(item[6])
            }
            for item in data
        ]
        save_kline_data(symbol, interval, formatted_data)
    return data

def get_interval_milliseconds(interval):
    interval_map = {
        '1m': 60000,
        '3m': 180000,
        '5m': 300000,
        '15m': 900000,
        '30m': 1800000,
        '1h': 3600000,
        '2h': 7200000,
        '4h': 14400000,
        '6h': 21600000,
        '8h': 28800000,
        '12h': 43200000,
        '1d': 86400000,
        '3d': 259200000,
        '1w': 604800000,
        '1M': 2592000000,
    }
    return interval_map.get(interval, 3600000)  # Default to 1h if interval not found

def process_kline_data(symbol, start_time, end_time, interval):
    data = fetch_kline_data(symbol, interval, start_time, end_time)
    df = pd.DataFrame(data, columns=['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime'])
    df['close'] = df['close'].astype(float)
    save_kline_data(symbol, interval, df.to_dict('records'))
    return df.to_dict('records')

@lru_cache(maxsize=100)
def get_macd(symbol, interval, start_time, end_time, fast=12, slow=26, signal=9):
    data = get_kline_data(symbol, interval, start_time, end_time)
    if not data:
        return None
    
    df = pd.DataFrame(data)
    df['close'] = df['close'].astype(float)
    df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')
    df.set_index('openTime', inplace=True)
    
    # Calculate MACD
    exp1 = df['close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    
    return {
        'macd': macd.tolist(),
        'signal': signal_line.tolist(),
        'histogram': histogram.tolist(),
        'timestamps': df.index.astype(int) // 10**6  # Convert to milliseconds
    }

@lru_cache(maxsize=100)
def get_rsi(symbol, interval, start_time, end_time, periods=14, ema=True):
    data = get_kline_data(symbol, interval, start_time, end_time)
    if not data:
        return None
    
    df = pd.DataFrame(data)
    df['close'] = df['close'].astype(float)
    df['openTime'] = pd.to_datetime(df['openTime'], unit='ms')
    df.set_index('openTime', inplace=True)
    
    # Calculate RSI
    close_delta = df['close'].diff()
    
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema:
        ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
    else:
        ma_up = up.rolling(window=periods).mean()
        ma_down = down.rolling(window=periods).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    
    return {
        'rsi': rsi.tolist(),
        'timestamps': df.index.astype(int) // 10**6  # Convert to milliseconds
    }