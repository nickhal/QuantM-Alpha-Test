# Crypto Data Processing and Visualization

This project provides a backend API for fetching and processing cryptocurrency data, as well as a frontend for visualizing the data.

## Features

- Fetch and store K-line (candlestick) data for various cryptocurrencies
- Calculate and provide MACD and RSI indicators
- Visualize candlestick charts with MACD and RSI indicators
- RESTful API for data retrieval
- React-based frontend for data visualization

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL

### Backend Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/crypto-data-processing.git
   cd crypto-data-processing
   ```

2. Set up a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r backend/requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the `backend` directory with the following content:

   ```
   DATABASE_URL=postgresql://yourusername:yourpassword@localhost/yourdatabase
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_API_SECRET=your_binance_api_secret
   ```

5. Initialize the database:

   ```
   python backend/database.py
   ```

6. Run the backend server:
   ```
   python backend/run.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Run the frontend development server:
   ```
   npm start
   ```

## API Documentation

### Endpoints

- `GET /api/kline`: Fetch K-line data

  - Query parameters:
    - `symbol`: Trading pair symbol (e.g., BTCUSDT)
    - `interval`: Time interval (e.g., 1m, 5m, 1h)
    - `startTime`: Start time in milliseconds
    - `endTime`: End time in milliseconds

- `GET /api/macd`: Fetch MACD indicator data

  - Query parameters:
    - `symbol`: Trading pair symbol
    - `interval`: Time interval

- `GET /api/rsi`: Fetch RSI indicator data

  - Query parameters:
    - `symbol`: Trading pair symbol
    - `interval`: Time interval

- `GET /api/symbols`: Fetch available trading pair symbols

## Running Tests

To run the backend tests:

```
python -m unittest discover backend/tests
```
