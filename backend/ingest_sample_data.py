import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001/api"

def generate_sample_data(symbol, interval, start_time, end_time, step):
    data = []
    current_time = start_time
    while current_time < end_time:
        price = 35000 + (current_time.timestamp() % 1000)  # Simple price variation
        kline = {
            "symbol": symbol,
            "interval": interval,
            "openTime": int(current_time.timestamp() * 1000),
            "open": price,
            "high": price + 100,
            "low": price - 100,
            "close": price + 50,
            "volume": 100 + (current_time.timestamp() % 100),
            "closeTime": int((current_time + step).timestamp() * 1000 - 1)
        }
        data.append(kline)
        current_time += step
    return data

def ingest_data(data):
    response = requests.post(f"{BASE_URL}/ingest", json=data)
    print(f"Ingestion response: {response.status_code}")
    print(response.json())

if __name__ == "__main__":
    now = datetime.now()
    start_time = now - timedelta(days=7)
    end_time = now

    intervals = {
        "1m": timedelta(minutes=1),
        "5m": timedelta(minutes=5),
        "60m": timedelta(hours=1)
    }

    for interval, step in intervals.items():
        print(f"Generating and ingesting data for {interval} interval")
        data = generate_sample_data("BTCUSD", interval, start_time, end_time, step)
        ingest_data(data)