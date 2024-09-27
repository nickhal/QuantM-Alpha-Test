import requests
from datetime import datetime
import time
from typing import List, Dict

BINANCE_BASE_URL = "https://api.binance.com/api/v3"

def fetch_kline_data(symbol: str, interval: str, start_time: int, end_time: int) -> List[Dict]:
    """
    Fetch K-line data from Binance API for a specific time range
    """
    url = f"{BINANCE_BASE_URL}/klines"
    all_klines = []
    
    while start_time < end_time:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000  # Maximum allowed by Binance
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        klines = response.json()
        
        if not klines:
            break
        
        all_klines.extend(klines)
        start_time = klines[-1][0] + 1  # Next start time is the last candle's close time + 1
        
        # Respect Binance API rate limits
        time.sleep(0.5)
    
    return [
        {
            "openTime": int(item[0]),
            "open": float(item[1]),
            "high": float(item[2]),
            "low": float(item[3]),
            "close": float(item[4]),
            "volume": float(item[5]),
            "closeTime": int(item[6])
        }
        for item in all_klines
    ]

# Remove the fetch_and_store_kline_data and start_data_fetching functions from here