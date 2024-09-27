import requests
from backend.config import BINANCE_API_URL, BINANCE_API_KEY, BINANCE_API_SECRET

def fetch_kline_data(symbol, interval, start_time, end_time):
    endpoint = f"{BINANCE_API_URL}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time
    }
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }
    
    response = requests.get(endpoint, params=params, headers=headers)
    response.raise_for_status()
    return response.json()