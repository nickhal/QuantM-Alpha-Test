from flask import Blueprint, request, jsonify
from backend.data.processing import process_kline_data, get_macd, get_rsi
from backend.data.storage import get_kline_data
from flask_cors import CORS
import asyncio
import logging

api = Blueprint('api', __name__)
CORS(api)

logger = logging.getLogger(__name__)

@api.route('/kline', methods=['GET'])
async def kline():
    try:
        symbol = request.args.get('symbol', 'BTCUSDT')
        interval = request.args.get('interval', '1m')
        start_time = int(request.args.get('startTime', 0))
        end_time = int(request.args.get('endTime', 0))
        
        logger.info(f"Fetching kline data for {symbol} with interval {interval}")
        data = await asyncio.to_thread(get_kline_data, symbol, interval, start_time, end_time)
        if not data:
            logger.info(f"No data found, processing new data for {symbol}")
            data = await asyncio.to_thread(process_kline_data, symbol, start_time, end_time, interval)
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in kline endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/macd', methods=['GET'])
async def macd():
    try:
        symbol = request.args.get('symbol', 'BTCUSDT')
        interval = request.args.get('interval', '1h')
        start_time = int(request.args.get('startTime', 0))
        end_time = int(request.args.get('endTime', 0))
        
        logger.info(f"Calculating MACD for {symbol} with interval {interval}")
        macd_data = await asyncio.to_thread(get_macd, symbol, interval, start_time, end_time)
        if not macd_data:
            logger.warning(f"No MACD data available for {symbol}")
            return jsonify({'macd': [], 'signal': [], 'histogram': [], 'timestamps': []}), 200
        
        return jsonify(macd_data)
    except Exception as e:
        logger.error(f"Error in MACD endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/rsi', methods=['GET'])
async def rsi():
    try:
        symbol = request.args.get('symbol', 'BTCUSDT')
        interval = request.args.get('interval', '1h')
        start_time = int(request.args.get('startTime', 0))
        end_time = int(request.args.get('endTime', 0))
        
        logger.info(f"Calculating RSI for {symbol} with interval {interval}")
        rsi_data = await asyncio.to_thread(get_rsi, symbol, interval, start_time, end_time)
        if not rsi_data:
            logger.warning(f"No RSI data available for {symbol}")
            return jsonify({'rsi': [], 'timestamps': []}), 200
        
        return jsonify(rsi_data)
    except Exception as e:
        logger.error(f"Error in RSI endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api.route('/symbols', methods=['GET'])
def symbols():
    try:
        symbols = ['BTCUSDT']
        logger.info("Fetching available symbols")
        return jsonify(symbols)
    except Exception as e:
        logger.error(f"Error in symbols endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500