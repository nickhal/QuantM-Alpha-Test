from flask import Blueprint
from backend.data.processing import get_kline_data, get_macd, get_rsi

api_bp = Blueprint('api', __name__)

# Your route definitions here