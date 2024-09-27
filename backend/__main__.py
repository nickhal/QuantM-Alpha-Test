from backend.app import create_app
from backend.data.processing import fetch_and_store_kline_data
import threading
import time

def continuous_data_fetch():
    symbol = 'BTCUSDT'
    intervals = ['1h', '4h', '1d']
    while True:
        for interval in intervals:
            fetch_and_store_kline_data(symbol, interval, 1)  # Fetch only the latest data point
        time.sleep(60)  # Wait for 1 minute before the next fetch

if __name__ == "__main__":
    app = create_app()
    
    # Start continuous data fetching in a separate thread
    fetch_thread = threading.Thread(target=continuous_data_fetch)
    fetch_thread.daemon = True
    fetch_thread.start()

    # Start the Flask app
    app.run(debug=True, port=5001)